import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

def entrenar_modelos(datos: pd.DataFrame):
    """
    Entrena modelos de predicción de retrasos (XGBoost con pipeline y CatBoost optimizado).
    Devuelve ambos modelos entrenados.
    """

    # ---------------------------
    # 1. Target: retraso grave >= 30 min
    # ---------------------------
    causas = ['RETRASO_SISTEMA_AEREO','RETRASO_SEGURIDAD',
              'RETRASO_AEROLINEA','RETRASO_AVION_TARDIO','RETRASO_CLIMA']
    datos["RETRASO_TOTAL"] = datos[causas].sum(axis=1)
    y = (datos["RETRASO_TOTAL"] >= 30).astype(int)

    # ---------------------------
    # 2. Feature engineering
    # ---------------------------
    datos["FECHA_COMPLETA"] = pd.to_datetime(
        datos[["ANO","MES","DIA"]].rename(columns={"ANO":"year","MES":"month","DIA":"day"})
    )

    datos["DIA_SEMANA"] = datos["FECHA_COMPLETA"].dt.dayofweek
    datos["ES_FIN_DE_SEMANA"] = datos["DIA_SEMANA"].isin([5,6]).astype(int)

    datos["TEMPORADA"] = pd.cut(datos["MES"],
                                bins=[0,3,6,9,12],
                                labels=["Verano","Otoño","Invierno","Primavera"],
                                right=True)

    datos["HORA_LLEGADA"] = pd.to_numeric(datos["HORA_LLEGADA"], errors="coerce").fillna(0).astype(int)
    datos["FRANJA_HORARIA_LLEGADA"] = pd.cut(datos["HORA_LLEGADA"],
                                             bins=[0,6,12,18,24],
                                             labels=["Madrugada","Mañana","Tarde","Noche"],
                                             right=False)

    datos["LLEGADA_PROGRAMA"] = pd.to_numeric(datos["LLEGADA_PROGRAMA"], errors="coerce").fillna(0).astype(int)
    datos["FRANJA_LLEGADA_PROGRAMA"] = pd.cut(datos["LLEGADA_PROGRAMA"],
                                              bins=[0,6,12,18,24],
                                              labels=["Madrugada","Mañana","Tarde","Noche"],
                                              right=False)

    # ---------------------------
    # 3. Features finales
    # ---------------------------
    X = datos[[
        "AEROLINEA","AEROPUERTO_ORIGEN","AEROPUERTO_DESTINO",
        "DISTANCIA","ANO","MES","DIA","ES_FIN_DE_SEMANA","TEMPORADA",
        "HORA_LLEGADA","FRANJA_HORARIA_LLEGADA",
        "LLEGADA_PROGRAMA","FRANJA_LLEGADA_PROGRAMA"
    ]]

    categorical_features = [
        "AEROLINEA","AEROPUERTO_ORIGEN","AEROPUERTO_DESTINO",
        "MES","DIA","TEMPORADA","FRANJA_HORARIA_LLEGADA","FRANJA_LLEGADA_PROGRAMA"
    ]
    numeric_features = ["DISTANCIA","ANO","ES_FIN_DE_SEMANA","HORA_LLEGADA","LLEGADA_PROGRAMA"]

    # ---------------------------
    # 4. Limpieza de datos
    # ---------------------------
    for col in categorical_features:
        X.loc[:, col] = X[col].astype(str).fillna("missing")

    for col in numeric_features:
        X.loc[:, col] = pd.to_numeric(X[col], errors="coerce")
        X.loc[:, col] = X[col].fillna(X[col].mean())

    # ---------------------------
    # 5. Split de datos
    # ---------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ---------------------------
    # 6. Entrenar modelos
    # ---------------------------
    # XGBoost con pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    xgb_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", XGBClassifier(
            eval_metric="logloss",
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        ))
    ])
    xgb_pipeline.fit(X_train, y_train)

    # CatBoost optimizado
    cat_model = CatBoostClassifier(
        iterations=1000,
        depth=5,
        learning_rate=0.03,
        random_seed=42,
        verbose=100,
        loss_function="Logloss",   # eval_metric se define aquí
        eval_metric="Logloss",
        class_weights=[1, len(y_train[y_train==0]) / len(y_train[y_train==1])]
    )

    cat_model.fit(
        X_train, y_train,
        cat_features=categorical_features,
        eval_set=(X_test, y_test),
        use_best_model=True
    )

    return xgb_pipeline, cat_model