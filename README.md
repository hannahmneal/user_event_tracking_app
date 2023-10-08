# **User Event Tracking Api Application**

## 🌐 **API**

### ⚙️ **Setup**

- Clone this repo and open the project in your IDE (I am using Visual Studio Code):
- To get started, from the project root create a `.env` file and copy-🍝 the contents of `.env.sample` into it (refer to the "Environment Variables" table below for local values)
- Create your virtual environment (for `venv` users, this is: `python3 -m venv api && source api/bin/activate`)
- Next, set up the database with: `make setup-db`. Before moving to the next step, confirm you see 'Started' for 'Container postgres' in your terminal, like this:
```
[+] Running 3/3
 ✔ Volume "user_event_tracking_app_db-data"  Created                                                                                                                                                   0.0s 
 ✔ Container postgres                        Started                                                                                                                                                   0.0s 
```
- To start the app itself, run: `make start-api`
- Before making any `Event` in the database, you need to create some `Person` rows (this is because an event is intended to be associated with a person). This can be done easily if you have Postman installed and upload the collection I included in `api/docs/User Events Api Application.postman_collection.json`.

<br/>


👇 Click the dropdown tables below for additional resources

<details>
<summary>Environment Variables</summary>

_While there is only one environment currently (local), variables for database connections, authentication, and other sensitive information would need to be changed for non-local development_.

| Env Variable | Local Value | Description & Usage |
| --- | --- | --- |
| `DB_HOST` | `"localhost"` | The host for the PostgreSQL database |
| `DB_NAME` | `"postgres"` | The name of the PostgreSQL database |
| `DB_PASS` | `"password"` | The password for the PostgreSQL database |
| `DB_PORT` | `6543` | The port for the PostgreSQL database |
| `DB_USER`  | `"dev"` |The user of the PostgreSQL database (PostgreSQL requires this) |
| `ENVIRONMENT` | `"local"` | Denotes the current development environment |
| `SHOW_ERROR_DETAILS` | `false` | Allows exception details to be surfaced directly from failing web requests as described [here]("https://www.neoteroi.dev/blacksheep/application/#handling-errors"). To avoid security issues, this is `false` by default and will only be `true` if `ENVIRONMENT="local"` |

</details>
<br/>

<details>
<summary>Tasks & Commands</summary>

<br/>

| Command | Description |
| --- | --- |
| `make start-api` | Starts the api (assuming the database is already running successfully) |
| `make setup-db` | Sets up PostgreSQL database in a docker container |

</details>

---

### 🔗 **Routes & Requests**

OpenApi Documentation can be found locally at http://127.0.0.1:8080/docs. Additionally, a Postman Collection has been included for convenience (see api/docs/User Events Api Application.postman_collection.json). Import it directly into Postman to begin playing with the api. It includes collection variables and pre-request scripts for dynamic POST requests, but it does not include environment variables. You will need to add an environment variable yourself called `base_url`. It's value should be `http://127.0.0.1:8080`.

For those who don't have Postman, Routes & Requests are included in the dropdowns below

<details>
<summary>GET Persons</summary>
<br/>

Route: `http://127.0.0.1:8080/persons`

Response: 
```
{
    "data": [
        {
            "id": "e67e0a09-b4bf-465b-9490-a1f284d2d090",
            "datetime_created": "2023-10-06T02:39:56.366948",
            "datetime_modified": "2023-10-06T02:39:56.366948",
            "email": "Effie.Abshire@test.mock",
            "events": [],
            "first_name": "Effie",
            "last_name": "Abshire",
            "role": "user"
        },
        {
            "id": "3ebec32b-49bb-455e-a0ae-8fbf6c440581",
            "datetime_created": "2023-10-06T02:41:02.502941",
            "datetime_modified": "2023-10-06T02:41:02.502941",
            "email": "Rosamond.Luettgen@test.mock",
            "events": [],
            "first_name": "Rosamond",
            "last_name": "Luettgen",
            "role": "admin"
        },
        {
            "id": "bea58cbf-0b80-4564-be18-29e258468f2e",
            "datetime_created": "2023-10-06T02:41:08.307449",
            "datetime_modified": "2023-10-05T21:56:47.467118",
            "email": "Scott.Summers@test.mock",
            "events": [],
            "first_name": "Scott",
            "last_name": "Summers",
            "role": "admin"
        }
    ],
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

<details>
<summary>GET Persons by id</summary>
<br/>

Route: `http://127.0.0.1:8080/persons/{id}`

Response: 
```
{
    "data": {
        "id": "bea58cbf-0b80-4564-be18-29e258468f2e",
        "datetime_created": "2023-10-06T02:41:08.307449",
        "datetime_modified": "2023-10-05T21:56:47.467118",
        "email": "Scott.Summers@test.mock",
        "events": [],
        "first_name": "Scott",
        "last_name": "Summers",
        "role": "admin"
    },
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

<details>
<summary>POST Persons</summary>
<br/>

Route: `http://127.0.0.1:8080/persons`

Request body: 
```
{
  "email": "kate.pryde@marauders.mock",
  "first_name": "Kate",
  "last_name": "Pryde",
  "role": 'admin'
}
```

Response: 
```
{
    "data": {
        "id": "e67e0a09-b4bf-465b-9490-a1f284d2d090",
        "datetime_created": "2023-10-06T02:39:56.366948",
        "datetime_modified": "2023-10-06T02:39:56.366948",
        "email": "kate.pryde@marauders.mock",
        "events": [],
        "first_name": "Kate",
        "last_name": "Pryde",
        "role": "admin"
    },
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 201
    }
}
```

</details>

<br/>

<details>
<summary>PUT Persons</summary>
<br/>

Route: `http://127.0.0.1:8080/persons/{id}`

Request body: 
```
{
  "id": "bea58cbf-0b80-4564-be18-29e258468f2e",
  "email": "Scott.Summers@test.mock",
  "events": [],
  "first_name": "Scott",
  "last_name": "Summers",
  "role": "admin"
}
```

Response: 
```
{
    "data": {
        "id": "bea58cbf-0b80-4564-be18-29e258468f2e",
        "datetime_created": "2023-10-06T02:41:08.307449",
        "datetime_modified": "2023-10-05T21:56:47.467118",
        "email": "Scott.Summers@test.mock",
        "events": [],
        "first_name": "Scott",
        "last_name": "Summers",
        "role": "admin"
    },
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

<details>
<summary>DELETE Persons</summary>
<br/>

Route: `http://127.0.0.1:8080/persons/{id}`

Request body: 
```
{
    "id": "7c56a5bc-6037-432f-bd4e-3606a744fcf4"
}
```

Response: 
```
{
    "data": null,
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

---

<details>
<summary>GET Events</summary>
<br/>

Route: `http://127.0.0.1:8080/events`

Params (optional): `?search="{keyword}"`

Response: 
```
{
    "data": [
        {
            "id": "3c492150-9ff3-493b-9b50-3c38bfca3baa",
            "datetime_created": "2023-10-06T10:53:05.830770",
            "event_type": "submitted_feedback",
            "person_id": "049bb5dd-91d2-464e-b049-07da3e8d2627"
        },
        {
            "id": "97406743-6987-44a8-bb97-d05da2f5f378",
            "datetime_created": "2023-10-06T10:53:28.421469",
            "event_type": "click",
            "person_id": "0fcf3634-9b0c-4ceb-ab53-7ba8edf3d5fa"
        },
        {
            "id": "274550f2-9660-4bf6-94e1-2aa6cc42982c",
            "datetime_created": "2023-10-06T10:53:30.265901",
            "event_type": "submitted_feedback",
            "person_id": "0fcf3634-9b0c-4ceb-ab53-7ba8edf3d5fa"
        },
        {
            "id": "9c65af1a-c109-4c17-9bf1-5f4bcac95e3c",
            "datetime_created": "2023-10-06T10:53:31.283195",
            "event_type": "signup",
            "person_id": "0fcf3634-9b0c-4ceb-ab53-7ba8edf3d5fa"
        }
    ],
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

<details>
<summary>GET Events by id</summary>
<br/>

Route: `http://127.0.0.1:8080/events/{id}`

Response: 
```
{
    "data": {
        "id": "62701308-809d-4302-b345-92ca72285194",
        "datetime_created": "2023-10-06T08:44:23.125253",
        "event_type": "signup",
        "person_id": "049bb5dd-91d2-464e-b049-07da3e8d2627"
    },
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

<details>
<summary>POST Events</summary>
<br/>

Route: `http://127.0.0.1:8080/events/{id}`

Request body:
```
{
  "event_type": "signup",
  "person_id": "9c65af1a-c109-4c17-9bf1-5f4bcac95e3c"
}
```

Response: 
```
{
    "data": {
        "id": "9c65af1a-c109-4c17-9bf1-5f4bcac95e3c",
        "datetime_created": "2023-10-06T10:53:31.283195",
        "event_type": "signup",
        "person_id": "0fcf3634-9b0c-4ceb-ab53-7ba8edf3d5fa"
    },
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 201
    }
}
```

</details>

<br/>

<details>
<summary>DELETE Events</summary>
<br/>

Route: `http://127.0.0.1:8080/events/{id}`

Request body:
```
{
    "id": "62701308-809d-4302-b345-92ca72285194",
    "person_id": "049bb5dd-91d2-464e-b049-07da3e8d2627"
}
```

Response: 
```
{
    "data": null,
    "response": {
        "details": "The request was successful",
        "message": "Ok",
        "status": 200
    }
}
```

</details>

<br/>

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

## 💬 **DISCUSSION**

_Originally I wanted to create an api that allowed for the creation of both events and users. I already had a boilerplate CRUD api that I was working on and it had Person objects so I thought, "Why not?". For this reason, `Persons` are included in the project. The linkage between `Person` and `Event` isn't complete but I'm still working on that. I focused my attention on the `Event` functionality, which includes the ability to search by a keyword._

I chose [blacksheep](https://www.neoteroi.dev/blacksheep/) for my framework because (A) I was already playing with it, (B) it's new and different to me, and (C) I am fascinated by its blend of Python + .NET. It seems like the best of both worlds and I was intrigued by the promise of maintainability, type safety, and speed of performance. I used [Piccolo ORM](https://github.com/piccolo-orm/piccolo) for database interactions because it was recommended by Blacksheep's [Roberto Prevato](https://github.com/Neoteroi/BlackSheep/commits?author=RobertoPrevato) but also because after a galumping through SQLAlchemy docs for what felt like decades, 30 minutes spent on Piccolo's offerings convinced me it was feature-rich and worth trying (the `auto_increment` option for a `Timestamp`, the [Playground](https://piccolo-orm.readthedocs.io/en/latest/piccolo/getting_started/playground.html), `piccolo admin`, and simple [Postgres setup](https://piccolo-orm.readthedocs.io/en/latest/piccolo/getting_started/setup_postgres.html) are all great examples). For data validation, I am using `Pydantic`, which handily ships with `Piccolo`.

As for architecture, I was going for a microservices approach. This is a small project so I began with a single file (`server.py`) which contains the database connection logic, routing, and 'service layer methods'. I do not enjoy how crowded it has become and I intend to simplify everything by separating `routes` from `service` logic and streamlining errors, exceptions, responses and if/else conditions.

After doing some light reading about events and event sourcing, I decided to use a very simple Event table structure and a `JSONB` string which can be searched with the `arrow` function provided by `Piccolo` (in the same way as a `->>` is used in raw SQL). After running into some limitations in my current knowledge, however, I left some comments and used `Varchar` for my simple event model. 

---

## 📔 **RESOURCES & REFERENCES**

[1] [Simple CRUD REST API with Blacksheep and Piccolo ORM by Carlos Armando Marcano Vargas](https://medium.com/@carlosmarcano2704/simple-crud-rest-api-with-blacksheep-and-piccolo-orm-698e6e85ae80)

[2] [Auto Migrations (from the Piccolo blog)](https://piccolo-orm.com/blog/auto-migrations/)

[3] [Piccolo ORM](https://piccolo-orm.readthedocs.io/_/downloads/en/latest/pdf/)

[4] ["How to Decide What Events to Track (+15 Examples)" by Levi Olmstead on Whatfix Blog](https://whatfix.com/blog/events-to-track/)

[5] ["Event Storage in Postgres" by Kasey Speakman](https://dev.to/kspeakman/event-storage-in-postgres-4dk2)

[6] ["Building an Event Storage" by Kasey Speakman](https://cqrs.wordpress.com/documents/building-event-storage/)

<!-- 👇 A "... .NET library for building applications using document-based approach and Event Sourcing." But the docs were good and I'd like to explore this tool library in the future, as it appears to be very new. A video about the library is here: https://www.youtube.com/watch?v=rrWweRReLZM -->
<!-- [7] [Marten as Event Store](https://martendb.io/events/) -->

---
