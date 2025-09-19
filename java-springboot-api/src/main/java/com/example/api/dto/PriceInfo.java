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

    public Double getPrice() { return this.price; }
    public String getCurrency() { return this.currency; }
    public String getAvailability() { return this.availability; }
}
