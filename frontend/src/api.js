/**
 * Centralized API utility for communicating with the backend.
 *
 * Responsibilities:
 * - Store and retrieve authentication token
 * - Attach auth headers automatically
 * - Handle unauthorized (401) responses gracefully
 *
 * This keeps network logic out of UI components
 * and follows separation of concerns.
 */

const API_URL = "http://127.0.0.1:8000";

// -------------------------------------------------------------------
// Token helpers
// -------------------------------------------------------------------
export function setToken(token) {
  if (token) {
    localStorage.setItem("token", token);
  } else {
    localStorage.removeItem("token");
  }
}

export function getToken() {
  return localStorage.getItem("token");
}

// -------------------------------------------------------------------
// Generic API request helper
// -------------------------------------------------------------------
export async function apiRequest(path, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  /**
   * If the backend returns 401 (Unauthorized),
   * it usually means the token is invalid or expired.
   * Clear local session data and force a reload
   * to return the user to the login screen.
   */
  if (response.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    localStorage.removeItem("is_admin");
    window.location.reload();
    return;
  }

  return response.json();
}
