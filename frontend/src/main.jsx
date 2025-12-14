/**
 * Application entry point.
 *
 * This file bootstraps the React application by:
 * - Creating the root React DOM container
 * - Applying a global Material UI theme
 * - Rendering the main App component
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider, createTheme } from "@mui/material/styles";

import "./index.css";
import App from "./App";

/* ------------------------------------------------------------------
    Global Material UI Theme
------------------------------------------------------------------- */
const theme = createTheme({
  palette: {
    primary: {
      main: "#66bb6a",
    },
    secondary: {
      main: "#ffd300",
    },
  },
});

/* ------------------------------------------------------------------
    Render application
------------------------------------------------------------------- */
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </StrictMode>
);
