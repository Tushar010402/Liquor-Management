# Liquor Shop Management System - Frontend

This is the frontend application for the Liquor Shop Management System, built with React, TypeScript, and Material-UI.

## Features

- Multi-role access (SaaS Admin, Tenant Admin, Manager, Assistant Manager, Executive)
- Inventory management
- Sales processing
- Cash management
- Financial reporting
- Multi-shop management
- Responsive design for desktop and mobile

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Liquor-Management.git
   cd Liquor-Management/liquor-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view the application in your browser.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in development mode.

### `npm test`

Launches the test runner in interactive watch mode.

### `npm run test:coverage`

Runs tests and generates a coverage report.

### `npm run test:ci`

Runs tests in CI mode (non-interactive).

### `npm run lint`

Lints the source code using ESLint.

### `npm run lint:fix`

Lints and automatically fixes issues where possible.

### `npm run format`

Formats the code using Prettier.

### `npm run build`

Builds the app for production to the `build` folder.

## Testing

The application includes comprehensive tests for components, contexts, and utilities. Tests are written using Jest and React Testing Library.

To run all tests:
```
npm test
```

To run tests with coverage:
```
npm run test:coverage
```

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── auth/         # Authentication-related components
│   ├── common/       # Common UI components
│   └── layout/       # Layout components (Header, Sidebar, etc.)
├── contexts/         # React contexts for state management
├── hooks/            # Custom React hooks
├── pages/            # Page components organized by user role
│   ├── auth/         # Authentication pages
│   ├── saas-admin/   # SaaS Admin pages
│   ├── tenant-admin/ # Tenant Admin pages
│   ├── manager/      # Manager pages
│   ├── assistant-manager/ # Assistant Manager pages
│   └── executive/    # Executive pages
├── services/         # API services
├── tests/            # Test files and utilities
├── theme/            # Theme configuration
├── types/            # TypeScript type definitions
└── utils/            # Utility functions
```

## Demo Accounts

For testing purposes, you can use the following demo accounts:

- SaaS Admin: saas@example.com / password
- Tenant Admin: tenant@example.com / password
- Manager: manager@example.com / password
- Assistant Manager: assistant@example.com / password
- Executive: executive@example.com / password

## License

This project is licensed under the MIT License - see the LICENSE file for details.
