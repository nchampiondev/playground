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

    public String getName() { return this.name; }
    public String getBrand() { return this.brand; }
    public String getModel() { return this.model; }
    public Object getSpecifications() { return this.specifications; }
    public List<PriceInfo> getPrices() { return this.prices; }
}
