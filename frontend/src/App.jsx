

import { useEffect, useState } from "react";
import {
  TextField,
  Button,
  Stack,
  Typography,
  Card,
  Divider,
  AppBar,
  Toolbar,
  Chip,
  Grid,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Pagination,
  Drawer,
  Badge,
  IconButton,
} from "@mui/material";

import "./App.css";
import { apiRequest, setToken } from "./api";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

const CATEGORIES = [
  "Indian",
  "Chocolate",
  "Bakery",
  "Candy",
  "Dessert",
  "General",
];

const CATEGORY_COLORS = {
  Indian: "#FF5C00",
  Chocolate: "#5D4037",
  Bakery: "#F9A825",
  Candy: "#D81B60",
  Dessert: "#6A1B9A",
  General: "#546E7A",
};

const ITEMS_PER_PAGE = 6;

function App() {
    // ------------------------------------------------------------------
  // Auth state
  // ------------------------------------------------------------------
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  // ------------------------------------------------------------------
  // Sweet & inventory state
  // ------------------------------------------------------------------
  const [sweets, setSweets] = useState([]);
  const [name, setName] = useState("");
  const [category, setCategory] = useState("General");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");

  // ------------------------------------------------------------------
  // Pagination
  // ------------------------------------------------------------------
  const [page, setPage] = useState(1);
  const totalPages = Math.ceil((sweets?.length || 0) / ITEMS_PER_PAGE);

  // ------------------------------------------------------------------
  // Editing & restocking
  // ------------------------------------------------------------------
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editQuantity, setEditQuantity] = useState("");
  const [editCategory, setEditCategory] = useState("General");
  const [restockAmounts, setRestockAmounts] = useState({});

  // ------------------------------------------------------------------
  // Search & filters
  // ------------------------------------------------------------------
  const [searchName, setSearchName] = useState("");
  const [searchCategory, setSearchCategory] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");

  // ------------------------------------------------------------------
  // Cart state
  // ------------------------------------------------------------------
  const [cart, setCart] = useState([]);
  const [cartQuantities, setCartQuantities] = useState({});
  const [showCart, setShowCart] = useState(false);

  const paginatedSweets = (sweets || []).slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  );


  // ---------- RESTORE LOGIN ----------
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedEmail = localStorage.getItem("email");
    const savedAdmin = localStorage.getItem("is_admin");

    if (savedToken && savedEmail) {
      setToken(savedToken);
      setEmail(savedEmail);
      setIsAdmin(savedAdmin === "true");
      setLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    setPage(1);
  }, [sweets]);


  // ---------- API ----------
  async function login() {
    const data = await apiRequest("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", data.email);
      localStorage.setItem("is_admin", data.is_admin);

      setToken(data.access_token);
      setIsAdmin(data.is_admin);
      setLoggedIn(true);
      loadSweets();
    } else {
      alert("Login failed");
    }
  }

  async function register() {
    const data = await apiRequest("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (data.id) {
      alert("Registration successful. Please login.");
      setMode("login");
      setPassword("");
    } else {
      alert("Registration failed");
    }
  }
  async function refreshAfter(action) {
    await action();
    loadSweets();
  }


  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    localStorage.removeItem("is_admin");

    setToken(null);
    setLoggedIn(false);
    setIsAdmin(false);
    setSweets([]);
    setPassword("");
  }

  async function loadSweets() {
    const data = await apiRequest("/api/sweets");
    setSweets(data);
  }

  async function searchSweets() {
    const params = new URLSearchParams();
    if (searchName) params.append("name", searchName);
    if (searchCategory) params.append("category", searchCategory);
    if (minPrice) params.append("min_price", minPrice);
    if (maxPrice) params.append("max_price", maxPrice);

    const data = await apiRequest(`/api/sweets/search?${params.toString()}`);
    setSweets(data);
  }

  async function addSweet() {
    await apiRequest("/api/sweets", {
      method: "POST",
      body: JSON.stringify({
        name,
        category,
        price: Number(price),
        quantity: Number(quantity),
      }),
    });

    setName("");
    setCategory("General");
    setPrice("");
    setQuantity("");

    loadSweets();
  }

  async function purchaseSweet(id) {
    await apiRequest(`/api/sweets/${id}/purchase`, { method: "POST" });
    loadSweets();
  }

  async function deleteSweet(id) {
  refreshAfter(() =>
    apiRequest(`/api/sweets/${id}`, { method: "DELETE" })
);
  }

  async function saveEdit(id) {
    await apiRequest(`/api/sweets/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: editName,
        price: Number(editPrice),
        quantity: Number(editQuantity),
        category: editCategory,
      }),
    });

    setEditingId(null);
    loadSweets();
  }

  async function restockSweet(id) {
    const amount = restockAmounts[id];

    if (!amount || amount <= 0) {
      alert("Enter a valid restock amount");
      return;
    }

    await apiRequest(`/api/sweets/${id}/restock`, {
      method: "POST",
      body: JSON.stringify({ amount: Number(amount) }),
    });

    setRestockAmounts((prev) => ({ ...prev, [id]: "" }));
    loadSweets();
  }





  function increaseQty(id, maxQty) {
    setCartQuantities((prev) => ({
      ...prev,
      [id]: Math.min((prev[id] || 1) + 1, maxQty),
    }));
  }

  function decreaseQty(id) {
    setCartQuantities((prev) => ({
      ...prev,
      [id]: Math.max((prev[id] || 1) - 1, 1),
    }));
  }
  function addToCart(sweet) {
    const qty = cartQuantities[sweet.id] || 1;

    setCart((prev) => {
      const existing = prev.find((i) => i.id === sweet.id);
      if (existing) {
        return prev.map((i) =>
          i.id === sweet.id
            ? { ...i, qty: i.qty + qty }
            : i
        );
      }
      return [...prev, { ...sweet, qty }];
    });

    setCartQuantities((prev) => ({ ...prev, [sweet.id]: 1 }));
  }

  function clearCart() {
    setCart([]);               // empty cart
    setCartQuantities({});     // reset all qty selectors
    setShowCart(false);        // close cart panel (optional UX)
  }

  function getRemainingStock(sweet) {
    const cartItem = cart.find((i) => i.id === sweet.id);
    const inCartQty = cartItem ? cartItem.qty : 0;
    return sweet.quantity - inCartQty;
  }


  // ---------- UI ----------
  return (
  <div className="app-bg">
    {!loggedIn ? (
      /* ================= LOGIN / REGISTER ================= */
      <div className="glass-card login-card">
        {/* App Title */}
        <Typography
          variant="h4"
          textAlign="center"
          fontWeight="bold"
          mb={0.5}
        >
          🍬 Sweet Shop
        </Typography>

        {/* Subtitle */}
        <Typography
          variant="body2"
          textAlign="center"
          sx={{ opacity: 0.85 }}
          mb={3}
        >
          TDD Kata: Sweet Shop Management System
        </Typography>

        {/* Login / Register heading */}
        <Typography variant="h6" textAlign="center" mb={2}>
          {mode === "login" ? "Login" : "Register"}
        </Typography>


        <Stack spacing={2}>
          <TextField
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {mode === "login" ? (
            <>
              <Button variant="contained" onClick={login}>
                Login
              </Button>
              <Button onClick={() => setMode("register")}>
                New user? Register
              </Button>
            </>
          ) : (
            <>
              <Button variant="contained" onClick={register}>
                Register
              </Button>
              <Button onClick={() => setMode("login")}>
                Back to Login
              </Button>
            </>
          )}
        </Stack>
        <Typography
          variant="caption"
          display="block"
          textAlign="center"
          sx={{ mt: 3, opacity: 0.7 }}
        >
          Done by: S GURU PRASAD
        </Typography>

      </div>
    ) : (
      /* ================= DASHBOARD ================= */
      <div className="dashboard-container">
        {/* TOP BAR */}
        <AppBar position="sticky" sx={{ mb: 3 }}>
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Typography variant="h6">🍬 Sweet Shop</Typography>

            <Stack direction="row" spacing={1} alignItems="center">
              {isAdmin && <Chip label="Admin" color="warning" size="small" />}

              <Typography variant="body2">{email}</Typography>

              <IconButton color="inherit" onClick={() => setShowCart(true)}>
                <Badge badgeContent={cart.length} color="error">
                  <ShoppingCartIcon />
                </Badge>
              </IconButton>


              <Button color="inherit" onClick={logout}>
                Logout
              </Button>
            </Stack>

          </Toolbar>
        </AppBar>

        <Typography
          variant="body1"
          textAlign="center"
          sx={{ mb: 3, color: '#FFD700' }}  // gold

        >
          Logged in as <b>{email}</b> {isAdmin && "(Admin)"}
        </Typography>



        {/* ================= SEARCH & FILTERS ================= */}
        <Card sx={{ p: 3, mb: 4 }}>
          <Typography fontWeight="bold" mb={2}>
            Search & Filters
          </Typography>

          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                label="Name"
                fullWidth
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
              />
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel shrink>Category</InputLabel>
                <Select
                  value={searchCategory}
                  displayEmpty
                  renderValue={(selected) =>
                    selected ? selected : "All Categories"
                  }
                  onChange={(e) => setSearchCategory(e.target.value)}
                >
                  <MenuItem value="">
                    <em>All Categories</em>
                  </MenuItem>
                  {CATEGORIES.map((cat) => (
                    <MenuItem key={cat} value={cat}>
                      {cat}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6} md={3}>
              <TextField
                label="Min Price"
                fullWidth
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
            </Grid>

            <Grid item xs={6} md={3}>
              <TextField
                label="Max Price"
                fullWidth
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </Grid>
          </Grid>

          <Stack direction="row" spacing={2} mt={3}>
            <Button variant="contained" onClick={searchSweets}>
              Search
            </Button>
            <Button variant="outlined" onClick={loadSweets}>
              Reset
            </Button>
          </Stack>
        </Card>

        {/* ================= ADD SWEET (ADMIN) ================= */}
        {isAdmin && (
          <Card sx={{ p: 3, mb: 4 }}>
            <Typography fontWeight="bold" mb={2}>
              Add Sweet
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <TextField
                  label="Sweet name"
                  fullWidth
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </Grid>

              <Grid item xs={12} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Category</InputLabel>
                  <Select
                    value={category}
                    label="Category"
                    onChange={(e) => setCategory(e.target.value)}
                  >
                    {CATEGORIES.map((cat) => (
                      <MenuItem key={cat} value={cat}>
                        {cat}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={6} md={3}>
                <TextField
                  label="Price"
                  fullWidth
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                />
              </Grid>

              <Grid item xs={6} md={3}>
                <TextField
                  label="Quantity"
                  fullWidth
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </Grid>
            </Grid>

            <Button
              sx={{ mt: 3 }}
              fullWidth
              variant="contained"
              color="success"
              onClick={addSweet}
            >
              Add Sweet
            </Button>
          </Card>
        )}

        {/* ================= SWEETS GRID ================= */}
        <Grid container spacing={3}>
          {paginatedSweets.map((s) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={s.id}>
              <Card className="sweet-card" sx={{ p: 2 }}>
                {editingId === s.id ? (
                  <>
                    <TextField
                      label="Name"
                      fullWidth
                      value={editName}
                      onChange={(e) => setEditName(e.target.value)}
                      sx={{ mb: 1 }}
                    />

                    <TextField
                      label="Price"
                      fullWidth
                      value={editPrice}
                      onChange={(e) => setEditPrice(e.target.value)}
                      sx={{ mb: 1 }}
                    />

                    <TextField
                      label="Quantity"
                      fullWidth
                      value={editQuantity}
                      onChange={(e) => setEditQuantity(e.target.value)}
                      sx={{ mb: 1 }}
                    />

                    <FormControl fullWidth sx={{ mb: 1 }}>
                      <InputLabel>Category</InputLabel>
                      <Select
                        value={editCategory}
                        label="Category"
                        onChange={(e) => setEditCategory(e.target.value)}
                      >
                        {CATEGORIES.map((cat) => (
                          <MenuItem key={cat} value={cat}>
                            {cat}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>

                    <Stack direction="row" spacing={1}>
                      <Button
                        size="small"
                        variant="contained"
                        onClick={() => saveEdit(s.id)}
                      >
                        Save
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => setEditingId(null)}
                      >
                        Cancel
                      </Button>
                    </Stack>
                  </>
                ) : (
                  <>
                    <Typography variant="h6">{s.name}</Typography>

                    <Chip
                      label={s.category}
                      size="small"
                      sx={{
                        mb: 1,
                        color: "#fff",
                        backgroundColor:
                          CATEGORY_COLORS[s.category] || "#607D8B",
                      }}
                    />

                    <Typography variant="body2" color="text.secondary">
                      ₹{s.price}
                    </Typography>

                    <Typography variant="body2" sx={{ mb: 1 }}>
                      Stock: {getRemainingStock(s)}

                    </Typography>

                    <Chip
                      label={getRemainingStock(s) > 0 ? "In Stock" : "Out of Stock"}
                      color={getRemainingStock(s) > 0 ? "success" : "error"}
                      size="small"
                    />


                    <Stack spacing={1} mt={2}>
                      {/* Quantity selector */}
                      <Stack direction="row" spacing={1} alignItems="center" justifyContent="center">
                        <Button
                          size="small"
                          variant="outlined"
                          disabled={(cartQuantities[s.id] || 1) <= 1}
                          onClick={() => decreaseQty(s.id)}
                        >
                          −
                        </Button>

                        <Typography fontWeight="bold">
                          {cartQuantities[s.id] || 1}
                        </Typography>

                        <Button
                          size="small"
                          variant="outlined"
                          disabled={getRemainingStock(s) <= (cartQuantities[s.id] || 1)}
                          onClick={() => increaseQty(s.id, getRemainingStock(s))}
                        >
                          +
                        </Button>

                      </Stack>

                      <Button
                        fullWidth
                        variant="contained"
                        color="success"
                        disabled={getRemainingStock(s) === 0}
                        onClick={() => addToCart(s)}
                      >
                        Add to Cart
                      </Button>

                      <Button
                        fullWidth
                        variant="outlined"
                        color="primary"
                        disabled={s.quantity === 0}
                        onClick={() => purchaseSweet(s.id)}
                      >
                        Purchase Now
                      </Button>

                        {isAdmin && (
                        <>
                          {/* ADMIN RESTOCK */}
                          <Stack direction="row" spacing={1} alignItems="center" mt={1}>
                            <TextField
                              size="small"
                              type="number"
                              label="Restock"
                              value={restockAmounts[s.id] || ""}
                              onChange={(e) =>
                                setRestockAmounts((prev) => ({
                                  ...prev,
                                  [s.id]: e.target.value,
                                }))
                              }
                              sx={{ width: 90 }}
                            />

                            <Button
                              size="small"
                              variant="contained"
                              color="primary"
                              onClick={() => restockSweet(s.id)}
                            >
                              Add
                            </Button>
                          </Stack>

                          {/* ADMIN EDIT / DELETE */}
                          <Stack direction="row" spacing={1} mt={1}>
                            <Button
                              size="small"
                              variant="outlined"
                              onClick={() => {
                                setEditingId(s.id);
                                setEditName(s.name);
                                setEditPrice(s.price);
                                setEditQuantity(s.quantity);
                                setEditCategory(s.category);
                              }}
                            >
                              Edit
                            </Button>

                            <Button
                              size="small"
                              variant="outlined"
                              color="error"
                              onClick={() => deleteSweet(s.id)}
                            >
                              Delete
                            </Button>
                          </Stack>
                        </>
                      )}

                        
                      
                    </Stack>
                  </>
                )}
              </Card>
            </Grid>
          ))}
        </Grid>


        {/* ================= PAGINATION ================= */}
        {totalPages > 1 && (
          <Stack alignItems="center" sx={{ mt: 4 }}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={(e, value) => setPage(value)}
              shape="rounded"
              color="primary"
            />
          </Stack>
        )}
        <Drawer
          anchor="right"
          open={showCart}
          onClose={() => setShowCart(false)}
        >
          <div style={{ width: 360, padding: 24 }}>
            <Typography variant="h6" mb={2}>
              🛒 Your Cart
            </Typography>

            {cart.length === 0 ? (
              <Typography color="text.secondary">
                Your cart is empty. Add some sweets 🍬
              </Typography>
            ) : (
              <>
                {cart.map((item) => (
                  <Stack
                    key={item.id}
                    direction="row"
                    justifyContent="space-between"
                    alignItems="center"
                    mb={1}
                  >
                    <Typography>
                      {item.name} × {item.qty}
                    </Typography>
                    <Typography>
                      ₹{item.price * item.qty}
                    </Typography>
                  </Stack>
                ))}

                <Divider sx={{ my: 2 }} />

                <Typography fontWeight="bold">
                  Total: ₹
                  {cart.reduce(
                    (sum, item) => sum + item.price * item.qty,
                    0
                  )}
                </Typography>

                {/* ✅ CLEAR CART BUTTON */}
                <Button
                  fullWidth
                  sx={{ mt: 2 }}
                  variant="outlined"
                  color="error"
                  onClick={clearCart}
                >
                  Clear Cart
                </Button>
              </>
            )}

            <Button
              fullWidth
              sx={{ mt: 2 }}
              variant="contained"
              onClick={() => setShowCart(false)}
            >
              Close
            </Button>
          </div>
        </Drawer>


      </div>
    )}
  </div>
);
}
export default App;