package com.etechs.frontend.service;

import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.etechs.frontend.dto.NormalizeRequest;

@Service
public class NormalizeService {

    private final RestTemplate restTemplate;
    private final String backendUrl;

    public NormalizeService(RestTemplate restTemplate, @Value("${backend.url}") String backendUrl) {
        this.restTemplate = restTemplate;
        this.backendUrl = backendUrl;
    }

    public Map<String, Object> normalizeGeneric(String collectionName, Map<String, Object> rawData) {
        NormalizeRequest request = new NormalizeRequest(collectionName, rawData);
        return restTemplate.postForObject(backendUrl + "/normalize", request, Map.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> normalizeWalletAssetMeta(Map<String, Object> rawData) {
        return restTemplate.postForObject(backendUrl + "/normalize/wallet_asset_meta", rawData, Map.class);
    }

    @SuppressWarnings("unchecked")
    public Map<String, Object> normalizeWalletTransactionMeta(Map<String, Object> rawData) {
        return restTemplate.postForObject(backendUrl + "/normalize/wallet_transaction_meta", rawData, Map.class);
    }
}
