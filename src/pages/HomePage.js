
import React from "react";
import { Container, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

   
  return (
    <Container maxWidth="md" sx={{ textAlign: "center", marginTop: "5rem" }}>
      <Typography variant="h3" gutterBottom>
        Welcome to AI Study Smart Assistant
      </Typography>
      <Typography variant="h6" color="textSecondary" paragraph>
        Select your learning path and start your journey toward becoming a developer or AI engineer.
      </Typography>
      <Button variant="contained" onClick={() => navigate("/courses")}>
        Explore Courses
      </Button>
    </Container>
  );
}


export default HomePage;
