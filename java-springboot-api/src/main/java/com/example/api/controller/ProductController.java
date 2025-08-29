package com.example.api.controller;

import com.example.api.dto.ProductResponse;
import com.example.api.service.ProductService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    private final ProductService productService;

    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping
    public List<ProductResponse> getAllProducts() {
        return productService.getAllProducts();
    }

    @GetMapping("/brand/{brand}")
    public List<ProductResponse> getProductsByBrand(@PathVariable String brand) {
        return productService.getProductsByBrand(brand);
    }

    @GetMapping("/model/{model}")
    public List<ProductResponse> getProductsByModel(@PathVariable String model) {
        return productService.getProductsByModel(model);
    }
}
