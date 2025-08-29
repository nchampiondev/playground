package com.example.api.service;

import com.example.api.dto.ProductResponse;
import com.example.api.model.Product;
import com.example.api.model.Price;
import com.example.api.repository.ProductRepository;
import com.example.api.repository.PriceRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class ProductService {

    private final ProductRepository productRepository;
    private final PriceRepository priceRepository;

    public ProductService(ProductRepository productRepository, PriceRepository priceRepository) {
        this.productRepository = productRepository;
        this.priceRepository = priceRepository;
    }

    public List<ProductResponse> getAllProducts() {
        return this.productRepository.findAll()
            .stream()
            .map(this::mapProductWithPrices)
            .collect(Collectors.toList());
    }

    public List<ProductResponse> getProductsByBrand(String brand) {
        return this.productRepository.findByBrand(brand)
            .stream()
            .map(this::mapProductWithPrices)
            .collect(Collectors.toList());
    }

    public List<ProductResponse> getProductsByModel(String model) {
        return this.productRepository.findByModel(model)
            .stream()
            .map(this::mapProductWithPrices)
            .collect(Collectors.toList());
    }

    private ProductResponse mapProductWithPrices(Product product) {
        List<Price> prices = this.priceRepository.findByProductId(product.getId());
        return new ProductResponse(product, prices);
    }
}
