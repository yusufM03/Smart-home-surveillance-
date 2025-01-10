# Smart-home-surveillance

This project was realized as part of the Cloud of Things module at the Higher School of Communication of Tunis, dedicated to create a smart home surveillance system.

Created by:
- Makhlouf Youssef
- Yaakoubi Skander


# Technologies

- Wildfly 34.0.1 final
- JDK 21.0.1
- Mosquitto broker
- MongoDB

# IoT components:

- Raspberry Pi 4 
- Pi Camera



# Deployment Machine
The Application is also hosted on a virtual machine accessible at https://securevision.me
With our school mail, we can get a 100$ voucher inside of Microsoft Azure. With this voucher, we can create a virtual machine capable of hosting the middleware, the mosquitto broker and the database. The virtual machine have the following characteristics:
- Ram: 4GB
- vCPUS: 2
- Ressource disk size: 8GB

# Cerfitication and grading
We have enabled HTTPS with letsencrypt TLS certificate with HSTS enabled as well, ensuring only secure connections are allowed to the middleware.
Enabling TLS1.3 only on wildfly helps to generate A grading on SSLabs.

