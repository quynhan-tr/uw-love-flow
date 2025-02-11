# uw love flow ~

![Project Logo](static/Logo.png)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About

**uw love flow** is a web application designed to facilitate a unique speed dating experience using personality and preference matching. It leverages the Flask framework and a custom matching algorithm to pair participants based on their responses to a series of questions.

## Features

- User registration with personality and preference-based matching
- Real-time gender distribution display
- Admin panel for managing users and matches
- Responsive design for mobile and desktop

## Installation

To get a local copy up and running, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/project-name.git
   cd project-name
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure you have a `.env` file with the correct database URL and other environment variables.

5. **Run the application:**

   ```bash
   flask run
   ```

## Usage

1. **Register as a user:**

   Visit the `/friendship-quiz` route to fill out the quiz and register.

2. **Check your match:**

   After the matching process, visit `/result` with your Discord handle to see your match.

3. **Admin operations:**

   Use the `/host-options` route to access admin functionalities like running the matching algorithm and managing users.

## Configuration

- **Environment Variables:**

  Ensure you have a `.env` file with the following variables:
  - `DATABASE_URL`: The URL for your database.
  - `ADMIN_PASSWORD`: Password for accessing admin routes.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
