package com.example.api.dto;

import com.example.api.model.Product;
import com.example.api.model.Price;

import java.util.List;
import java.util.stream.Collectors;

public class ProductResponse {
    private String name;
    private String brand;
    private String model;
    private Object specifications;
    private List<PriceInfo> prices;

    public ProductResponse(Product product, List<Price> prices) {
        this.name = product.getName();
        this.brand = product.getBrand();
        this.model = product.getModel();
        this.specifications = product.getSpecifications();
        this.prices = prices.stream()
                .map(p -> new PriceInfo(p.getPrice(), p.getCurrency(), p.getAvailability()))
                .collect(Collectors.toList());
    }

    // Getters
    public String getName() { return name; }
    public String getBrand() { return brand; }
    public String getModel() { return model; }
    public Object getSpecifications() { return specifications; }
    public List<PriceInfo> getPrices() { return prices; }
}
