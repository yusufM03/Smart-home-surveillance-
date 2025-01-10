package com.supcom.cot.securevision.repositories;

import com.supcom.cot.securevision.entities.Log;
import jakarta.data.repository.CrudRepository;
import jakarta.data.repository.Repository;

import java.util.stream.Stream;

@Repository
public interface LogRepository extends CrudRepository<Log, String> {

    Stream<Log> findAll();

}
