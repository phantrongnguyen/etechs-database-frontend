package com.etechs.frontend.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.etechs.frontend.service.NormalizeService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

@Controller
public class NormalizeController {

    private final NormalizeService normalizeService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public NormalizeController(NormalizeService normalizeService) {
        this.normalizeService = normalizeService;
    }

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @GetMapping("/normalize/generic")
    public String genericForm() {
        return "generic-form";
    }

    @GetMapping("/normalize/wallet-asset-meta")
    public String walletAssetMetaForm() {
        return "asset-meta-form";
    }

    @GetMapping("/normalize/wallet-transaction-meta")
    public String walletTransactionMetaForm() {
        return "transaction-meta-form";
    }

    @PostMapping("/normalize/generic")
    public String normalizeGeneric(
            @RequestParam String collectionName,
            @RequestParam String rawData,
            Model model) {
        Map<String, Object> parsedData = parseJson(rawData);
        Map<String, Object> result = normalizeService.normalizeGeneric(collectionName, parsedData);
        model.addAttribute("result", toPrettyJson(result));
        model.addAttribute("endpoint", "Generic: " + collectionName);
        return "result";
    }

    @PostMapping("/normalize/wallet-asset-meta")
    public String normalizeWalletAssetMeta(
            @RequestParam String assetId,
            @RequestParam String displayName,
            @RequestParam String iconUrl,
            @RequestParam(required = false) String description,
            @RequestParam String earnedAt,
            @RequestParam String sourceRefType,
            @RequestParam String sourceRefId,
            @RequestParam(defaultValue = "false") boolean isTradable,
            Model model) {

        Map<String, Object> source = new HashMap<>();
        source.put("ref_type", sourceRefType);
        source.put("ref_id", sourceRefId);

        Map<String, Object> rawData = new HashMap<>();
        rawData.put("asset_id", assetId);
        rawData.put("display_name", displayName);
        rawData.put("icon_url", iconUrl);
        rawData.put("description", description.isEmpty() ? null : description);
        rawData.put("earned_at", earnedAt);
        rawData.put("source", source);
        rawData.put("is_tradable", isTradable);

        Map<String, Object> result = normalizeService.normalizeWalletAssetMeta(rawData);
        model.addAttribute("result", toPrettyJson(result));
        model.addAttribute("endpoint", "wallet_asset_meta");
        return "result";
    }

    @PostMapping("/normalize/wallet-transaction-meta")
    public String normalizeWalletTransactionMeta(
            @RequestParam String txId,
            @RequestParam(required = false) String note,
            @RequestParam String triggeredBy,
            @RequestParam int balanceBefore,
            @RequestParam int balanceAfter,
            @RequestParam(required = false) String receiptUrl,
            Model model) {

        Map<String, Object> snapshot = new HashMap<>();
        snapshot.put("balance_before", balanceBefore);
        snapshot.put("balance_after", balanceAfter);

        Map<String, Object> rawData = new HashMap<>();
        rawData.put("tx_id", txId);
        rawData.put("note", note != null && !note.isEmpty() ? note : null);
        rawData.put("triggered_by", triggeredBy);
        rawData.put("snapshot", snapshot);
        rawData.put("receipt_url", receiptUrl != null && !receiptUrl.isEmpty() ? receiptUrl : null);

        Map<String, Object> result = normalizeService.normalizeWalletTransactionMeta(rawData);
        model.addAttribute("result", toPrettyJson(result));
        model.addAttribute("endpoint", "wallet_transaction_meta");
        return "result";
    }

    private Map<String, Object> parseJson(String json) {
        try {
            return objectMapper.readValue(json, Map.class);
        } catch (Exception e) {
            throw new RuntimeException("Invalid JSON: " + e.getMessage());
        }
    }

    private String toPrettyJson(Object obj) {
        try {
            return objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(obj);
        } catch (JsonProcessingException e) {
            return obj.toString();
        }
    }
}
