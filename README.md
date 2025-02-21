# Slide Designer Server

Slide Designer Server is a RESTful API designed to support a web-based slide creation and editing application. It provides endpoints for managing slides and user sessions, facilitating seamless integration with front-end components.

## Features

- **Slide Management**: Create, update, delete, and retrieve slides.
- **User Sessions**: Maintain user sessions to ensure a personalized experience.
- **WebSocket Support**: Real-time updates and collaboration features.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **WebSockets**: Enables real-time communication between the server and clients.
- **Pydantic**: Data validation and settings management using Python type annotations.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zavu1on/slide-designer-server.git
   cd slide-designer-server
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   - Ensure you have a PostgreSQL database running.
   - Update the `config.py` file with your database credentials.

## Configuration

- **Configuration File**:
  - `config.py`: Contains default configurations which can be overridden by environment variables.

## Running the Application

Start the FastAPI development server:

```bash
fastapi dev main.py
```

The application will be accessible at `http://127.0.0.1:8000`.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
