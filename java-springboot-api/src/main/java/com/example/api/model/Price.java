package com.example.api.model;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.Instant;

@Document(collection = "prices")
public class Price {

    @Id
    private ObjectId id;

    @Field("product_id")
    private ObjectId productId;

    @Field("website_id")
    private ObjectId websiteId;

    private Double price;
    private String currency;

    @Field("product_url")
    private String productUrl;

    private String availability;

    @Field("scraped_at")
    private Instant scrapedAt;

    public ObjectId getId() {
        return this.id;
    }

    public void setId(ObjectId id) {
        this.id = id;
    }

    public ObjectId getProductId() {
        return this.productId;
    }

    public void setProductId(ObjectId productId) {
        this.productId = productId;
    }

    public ObjectId getWebsiteId() {
        return this.websiteId;
    }

    public void setWebsiteId(ObjectId websiteId) {
        this.websiteId = websiteId;
    }

    public Double getPrice() {
        return this.price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public String getCurrency() {
        return this.currency;
    }

    public void setCurrency(String currency) {
        this.currency = currency;
    }

    public String getProductUrl() {
        return this.productUrl;
    }

    public void setProductUrl(String productUrl) {
        this.productUrl = productUrl;
    }

    public String getAvailability() {
        return this.availability;
    }

    public void setAvailability(String availability) {
        this.availability = availability;
    }

    public Instant getScrapedAt() {
        return this.scrapedAt;
    }

    public void setScrapedAt(Instant scrapedAt) {
        this.scrapedAt = scrapedAt;
    }
}
