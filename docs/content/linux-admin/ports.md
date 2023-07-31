---
title: Ports in Linux

---

The webservers listen to **port 80** for http and **port 443** for https. What about other ports?

Trying to document my observations here. These things might differ if customized for some reason. we can check this with the command `lsof -i -P -n | grep LISTEN` on Linux.

| Port  | Service          |
| :---: | ---------------- |
|  80   | http connection  |
|  443  | https connection |
| 1313  | Hugo server      |
| 3306  | MySQL            |
| 5000  | Flask            |
| 5432  | PostgreSQL       |
| 6379  | Redis            |
