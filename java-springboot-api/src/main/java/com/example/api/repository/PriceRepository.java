package com.example.api.repository;

import org.bson.types.ObjectId;
import com.example.api.model.Price;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface PriceRepository extends MongoRepository<Price, ObjectId> {
    List<Price> findByProductId(ObjectId productId);
}
