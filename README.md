# FYN-Find-Your-Network-Live-Your-World
FYN is a social media app where users can share short videos, chat in real time, and join fitness or lifestyle communities.
Dưới đây là phiên bản README với ngôn ngữ tiếng Anh và sử dụng các tag trong file README để các chữ đẹp hơn:

**README**
================

**Project Name:** Social Network Multi-Platform Based on Microservices Architecture
--------------------------------------------------------

**Introduction**
===============

This project aims to build a multi-platform social network based on the microservices architecture. The social network will provide features such as user registration, login, viewing posts and reels, real-time chat,... This project utilizes modern technologies like Java (Spring Boot), Python (FastAPI) and PostgreSQL.

**System Description**
=====================

The social network system is divided into independent services:

1. **Auth Service**
-----------------

	* User Management:
		+ Registration
		+ Login
		+ Forgot Password
		+ OTP Verification (Optional)
	* Technology Stack: Java (Spring Boot), PostgreSQL
2. **UserService**
------------------

	* User Profile Management:
		+ Update Profile
		+ Search Users
		+ Follow/Unfollow Users
	* Technology Stack: Java (Spring Boot), PostgreSQL
3. **PostService**
-----------------

	* Post Management:
		+ Create New Post
		+ Edit Post
		+ Delete Post
		+ View Feed Posts
		+ Add Comments and Likes for Posts
	* Technology Stack: Java (Spring Boot), PostgreSQL
4. **ReelService**
------------------

	* Reel Management:
		+ Create New Reel
		+ Edit Reel
		+ Delete Reel
		+ View Feed Reels
		+ Add Comments and Likes for Reels
	* Technology Stack: Java (Spring Boot), PostgreSQL
5. **ChatService**
------------------

	* Real-time Chat:
		+ Send Text Messages and Linked Posts/Reels
		+ Receive Text Messages and Linked Posts/Reels
		+ Save Conversation History
	* Technology Stack: Python (FastAPI), PostgreSQL

**Key Features**
================

* User Registration/Login
* View Feed Posts/Reels
* Update Profile
* Follow/Unfollow Users
* Real-time Chat

**Technology Stack**
=====================

* Programming Languages: Java (Spring Boot), Python (FastAPI)
* Database: PostgreSQL
* Video Processing: FFmpeg (via worker process)
* Message Queue: RabbitMQ or In-Memory Cache
* Search Engine (Optional): Elasticsearch

**Development Guide**
====================

To develop this project, you need to follow these steps:

1. Install required technologies and libraries.
2. Create independent services for each module.
3. Add new features and functionality to each service.
4. Integrate and connect between services.

**Note**
--------

This project is still under development and may require additional configuration or setup to run effectively.

Hope this information is helpful! If you have any questions or need further assistance, please don't hesitate to contact us.