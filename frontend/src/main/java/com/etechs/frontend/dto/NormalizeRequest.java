package com.etechs.frontend.dto;

import java.util.Map;

public class NormalizeRequest {
    private String collectionName;
    private Map<String, Object> rawData;

    public NormalizeRequest() {}

    public NormalizeRequest(String collectionName, Map<String, Object> rawData) {
        this.collectionName = collectionName;
        this.rawData = rawData;
    }

    public String getCollectionName() { return collectionName; }
    public void setCollectionName(String collectionName) { this.collectionName = collectionName; }
    public Map<String, Object> getRawData() { return rawData; }
    public void setRawData(Map<String, Object> rawData) { this.rawData = rawData; }
}
