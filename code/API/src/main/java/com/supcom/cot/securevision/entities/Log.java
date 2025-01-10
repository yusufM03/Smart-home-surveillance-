package com.supcom.cot.securevision.entities;

import jakarta.nosql.Entity;
import jakarta.nosql.Id;
import jakarta.nosql.Column;
import jakarta.json.bind.annotation.JsonbVisibility;

@Entity
@JsonbVisibility(FieldPropertyVisibilityStrategy.class)
public class Log {

    @Id
    private String id;
    @Column
    private String timestamp;
    @Column
    private String detectedClass;

    public Log() {}

    public Log(String id, String timestamp, String detectedClass) {
        this.id = id;
        this.timestamp = timestamp;
        this.detectedClass = detectedClass;
    }



    // Getter and Setter methods
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getDetectedClass() {
        return detectedClass;
    }

    public void setDetectedClass(String detectedClass) {
        this.detectedClass = detectedClass;
    }


    @Override
    public String toString() {
        return "Log{" +
                "id='" + id + '\'' +
                ", timestamp='" + timestamp + '\'' +
                ", detectedClass='" + detectedClass + '\'' +
                '}';
    }
}
