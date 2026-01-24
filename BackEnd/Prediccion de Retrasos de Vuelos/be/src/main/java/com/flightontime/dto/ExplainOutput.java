package com.flightontime.dto;

import java.util.List;
import java.util.Map;

public class ExplainOutput {
    private List<Double> shap_values;
    private Double base_value;
    private List<String> features;
    private Map<String, Object> feature_values;
    private Double probabilidad;
    private Double debug_shap_rebuilt;

    // GETTERS Y SETTERS

    public List<Double> getShap_values() {
        return shap_values;
    }

    public void setShap_values(List<Double> shap_values) {
        this.shap_values = shap_values;
    }

    public Double getBase_value() {
        return base_value;
    }

    public void setBase_value(Double base_value) {
        this.base_value = base_value;
    }

    public List<String> getFeatures() {
        return features;
    }

    public void setFeatures(List<String> features) {
        this.features = features;
    }

    public Map<String, Object> getFeature_values() {
        return feature_values;
    }

    public void setFeature_values(Map<String, Object> feature_values) {
        this.feature_values = feature_values;
    }

    public Double getProbabilidad() {
        return probabilidad;
    }

    public void setProbabilidad(Double probabilidad) {
        this.probabilidad = probabilidad;
    }

    public Double getDebug_shap_rebuilt() {
        return debug_shap_rebuilt;
    }

    public void setDebug_shap_rebuilt(Double debug_shap_rebuilt) {
        this.debug_shap_rebuilt = debug_shap_rebuilt;
    }
}
