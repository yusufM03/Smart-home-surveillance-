package com.supcom.cot.securevision.boundaries;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import com.supcom.cot.securevision.util.Argon2Utility;
import java.util.function.Supplier;
import com.supcom.cot.securevision.entities.User;
import com.supcom.cot.securevision.repositories.UserRepository;

@ApplicationScoped
@Path("user")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class SignUpEndpoint {
    private static final Supplier<WebApplicationException> NOT_FOUND =
            () -> new WebApplicationException(Response.Status.NOT_FOUND);

    @Inject
    private UserRepository repository;

    @POST // Post method that receives User credentials from sign up in JSON format and saves it in the database
    public Response save(User user) {
        try {
            repository.findById(user.getmail()).orElseThrow(); // If User already exists , the request cannot go through
            return Response.status(Response.Status.UNAUTHORIZED).entity("{\"message\":\"user already exists!!!\"}").build();
        } catch (Exception e) {
            String password = user.getpassword();
            String passwordhash = Argon2Utility.hash(password.toCharArray()); // Hash the password tapped by the user before saving it in the database
            User userhash = new User(user.getmail(), user.getuserName(), passwordhash, user.getPermissionLevel()); //create new User entity with the new hashed password
            repository.save(userhash); // save the data in MongoDB
            return Response.ok().entity("{\"username created \":\"" + userhash.getuserName() + "\"}").build();
        }


    }
}
