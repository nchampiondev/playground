package com.example.api.dto;

public class PriceInfo {
    private Double price;
    private String currency;
    private String availability;

    public PriceInfo(Double price, String currency, String availability) {
        this.price = price;
        this.currency = currency;
        this.availability = availability;
    }

    // Getters
    public Double getPrice() { return price; }
    public String getCurrency() { return currency; }
    public String getAvailability() { return availability; }
}
