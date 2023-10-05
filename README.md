# **User Event Tracking Api Application**

OpenApi Documentation can be found locally at http://127.0.0.1:8080/docs

## 🌐 **API**

### ⚙️ **Setup**

After cloning this repo and opening the project in your IDE (I am using Visual Studio Code), you should see a project structure similar to this:
```
.
├── api
│   ├── db
│   │   ├── piccolo_app.py
│   │   ├── piccolo_migrations
│   │   └── tables
│   │       └── person.py
│   ├── constants
│   ├── ├── constants.py
│   ├── models
│   │   └── person.py
│   ├── server.py
│   └── tools.py
├── compose-dev.yaml
├── docker-compose.yml
├── Dockerfile
├── .env
├── .env.sample
├── piccolo_conf.py
├── Makefile
├── Readme.md
└── requirements.txt
```

- To get started, from the project root create a `.env` file and copy-🍝 the contents of `.env.sample` into it (refer to the "Environment Variables" table below for local values)
- Create your virtual environment (for `venv` users, this is: `python3 -m venv api && source api/bin/activate`)
- Next, set up the database with: `make setup-db`. Before moving to the next step, confirm you see 'Started' for 'Container postgres' in your terminal, like this:
```
[+] Running 3/3
 ✔ Volume "user_event_tracking_app_db-data"  Created                                                                                                                                                   0.0s 
 ✔ Container postgres                        Started                                                                                                                                                   0.0s 
```
- To start the app itself, run: `make start-api`

<details>
<summary>Environment Variables</summary>

_Variables for database connections, authentication, and other sensitive information must be changed for non-local development_.

| Env Variable | Local Value | Description & Usage |
| --- | --- | --- |
| `DB_HOST` | `"localhost"` | The host for the PostgreSQL database |
| `DB_NAME` | `"postgres"` | The name of the PostgreSQL database |
| `DB_PASS` | `"password"` | The password for the PostgreSQL database |
| `DB_PORT` | `6543` | The port for the PostgreSQL database |
| `DB_USER`  | `"dev"` |The user of the PostgreSQL database (PostgreSQL requires this) |
| `ENVIRONMENT` | `"local"` | Denotes the current development environment |
| `SHOW_ERROR_DETAILS` | `False` | Allows exception details to be surfaced directly from failing web requests as described [here]("https://www.neoteroi.dev/blacksheep/application/#handling-errors"). To avoid security issues, this is `False` by default and will only be `True` when `ENVIRONMENT="local"` |

</details>
<br/>

---

### 🟢 **Startup & Commands**

A table containing the startup and task commands is produced below

<details>
<summary>Startup & Task Commands</summary>

<br/>

| Command | Description |
| --- | --- |
| `make start-api` | Starts the api (assuming the database is already running successfully) |
| `make setup-db` | Sets up PostgreSQL database in a docker container |

</details>

---

### 🗄️ **Data & Migrations**

Migrations are managed with the `piccolo` package.

New migrations need to be created whenever there is a change to the database schema. To create a new migration, use the following (always include a brief description): `piccolo migrations new db --desc="good description of migration here"`.

To apply the migration, use `piccolo migrations forwards all`.

<!-- #### 😇 **Best Practices**

---

## 🦄 **APP (UI)**

---

### ⚙️ **Setup** -->

---

## 📔 **RESOURCES & REFERENCES**

[1] [Simple CRUD REST API with Blacksheep and Piccolo ORM by Carlos Armando Marcano Vargas](https://medium.com/@carlosmarcano2704/simple-crud-rest-api-with-blacksheep-and-piccolo-orm-698e6e85ae80)

[2] [Auto Migrations (from the Piccolo blog)](https://piccolo-orm.com/blog/auto-migrations/)

[3] [Piccolo ORM](https://piccolo-orm.readthedocs.io/_/downloads/en/latest/pdf/)

---
