package com.example.api.repository;

import com.example.api.model.Product;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.List;

public interface ProductRepository extends MongoRepository<Product, String> {
    List<Product> findByBrand(String brand);
    List<Product> findByModel(String model);
}
