
**Project Name:** FYN-Find-Your-Network-Live-Your-World
FYN is a social media app where users can share short videos, chat in real time, and join fitness or lifestyle communities.
Dưới đây là phiên bản README với ngôn ngữ tiếng Anh và sử dụng các tag trong file README để các chữ đẹp hơn:

--------------------------------------------------------

**Introduction**
===============

This project aims to build a multi-platform social network based on the microservices architecture. The social network will provide features such as user registration, login, viewing posts and reels, real-time chat,... This project utilizes modern technologies like Java (Spring Boot), Python (FastAPI) và PostgreSQL.

**System Description**
=====================

The social network system is divided into independent services:

1. **Auth Service**
-----------------

	* Tác vụ:
		+ Registration: tạo mới tài khoản người dùng
		+ Login: xác thực tài khoản người dùng
		+ Forgot Password: gửi lại mật khẩu cho người dùng
		+ OTP Verification (Optional): xác thực mã OTP
	* Technology Stack: Java (Spring Boot), PostgreSQL

2. **UserService**
------------------

	* Tác vụ:
		+ Update Profile: cập nhật thông tin hồ sơ người dùng
		+ Search Users: tìm kiếm người dùng
		+ Follow/Unfollow Users: theo dõi hoặc bỏ theo dõi người dùng khác
	* Technology Stack: Java (Spring Boot), PostgreSQL

3. **PostService**
-----------------

	* Tác vụ:
		+ Create New Post: tạo mới bài viết
		+ Edit Post: chỉnh sửa bài viết
		+ Delete Post: xóa bài viết
		+ View Feed Posts: xem feed bài viết
		+ Add Comments and Likes for Posts: thêm bình luận và like cho bài viết
	* Technology Stack: Java (Spring Boot), PostgreSQL

4. **ReelService**
------------------

	* Tác vụ:
		+ Create New Reel: tạo mới reel
		+ Edit Reel: chỉnh sửa reel
		+ Delete Reel: xóa reel
		+ View Feed Reels: xem feed reel
		+ Add Comments and Likes for Reels: thêm bình luận và like cho reel
	* Technology Stack: Java (Spring Boot), PostgreSQL

5. **ChatService**
------------------

	* Tác vụ:
		+ Send Text Messages and Linked Posts/Reels: gửi tin nhắn văn bản và liên kết bài viết/reel
		+ Receive Text Messages and Linked Posts/Reels: nhận tin nhắn văn bản và liên kết bài viết/reel
		+ Save Conversation History: lưu lịch sử trò chuyện
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