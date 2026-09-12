## Project Structure

The project follows a modular Django architecture to keep the code clean, scalable, and maintainable.

```text
Smartphone_Recommendation_System/

│
├── config/
│   ├── settings.py          # Django project settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   │
│   ├── smartphones/
│   │   ├── models.py        # Smartphone database models
│   │   ├── serializers.py   # API data serialization
│   │   ├── views.py         # Smartphone views/API endpoints
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── users/
│   │   ├── models.py        # User preference models
│   │   ├── views.py
│   │   └── serializers.py
│   │
│   ├── recommendation/
│   │   ├── engine.py        # Recommendation logic
│   │   ├── scoring.py       # Weighted scoring algorithms
│   │   └── services.py      # Recommendation services
│   │
│   └── common/
│       ├── utils.py         # Shared helper functions
│       └── constants.py
│
├── data/
│   └── smartphone_data.json # Initial smartphone dataset
│
├── tests/
│   ├── test_models.py
│   ├── test_api.py
│   └── test_recommendation.py
│
├── docker/
│   └── Dockerfile
│
├── requirements.txt
├── docker-compose.yml
├── manage.py
└── README.md
```

## Structure Explanation

### config/

Contains the main Django project configuration:

* Database settings
* Installed applications
* Global URL routing
* Server configuration

### smartphones/

Responsible for managing smartphone data.

Responsibilities:

* Smartphone database models
* Device specifications
* API endpoints
* Smartphone management

### users/

Handles user-related features.

Responsibilities:

* User accounts
* User preferences
* Recommendation requirements

### recommendation/

The core of the project.

Responsibilities:

* Analyze user preferences
* Compare smartphone features
* Calculate recommendation scores
* Rank suitable smartphones

### common/

Contains reusable components shared across applications.

Examples:

* Helper functions
* Constants
* Common utilities

### data/

Stores initial or imported smartphone datasets.

The project can receive data from the separate Smartphone Price Tracker project.

### tests/

Contains automated tests for:

* Database models
* API functionality
* Recommendation algorithms

### docker/

Contains containerization configuration for running the project consistently in different environments.
