package com.supcom.cot.securevision.boundaries;

import com.supcom.cot.securevision.entities.Log;
import com.supcom.cot.securevision.repositories.LogRepository;
import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.stream.Collectors;

@Path("/logs") //
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class LogEndpoint {

    @Inject
    private LogRepository logRepository;

    // Get all logs
    @GET
    public Response getAllLogs() {
        List<Log> logs = logRepository.findAll()
                .collect(Collectors.toList());
        return Response.ok(logs).build();
    }

    // Save a new log
    @POST
    public Response saveLog(Log log) {
        logRepository.save(log);
        return Response.status(Response.Status.CREATED)
                .entity("Log saved successfully")
                .build();
    }
}
