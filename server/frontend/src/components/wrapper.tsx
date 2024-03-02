import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
const drawerWidth = 200;
import Link from "next/link";
import React, { useState, useEffect } from "react";

//**This component is by default present on all pages*/
const Wrapper = () => {
  const [serverStatus, setServerStatus] = useState("checking...");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const checkIfBackendIsUpRequest = new Request(
          "http://127.0.0.1:8000/healthcheck",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              text: "healthy",
            }),
          }
        );

        const response = await fetch(checkIfBackendIsUpRequest);

        if (response.ok) {
          const data = await response.json();
          // Assuming your healthcheck returns 'healthy' if things are good
          if (data === "healthy") {
            setServerStatus("server is up");
          } else {
            setServerStatus("server is down");
          }
        } else {
          setServerStatus("server is down");
        }
      } catch (error) {
        console.error("Healthcheck error:", error);
        setServerStatus("server is down");
      }
    };

    // Initial check
    checkHealth();

    // Repeated check every 5 seconds
    const intervalId = setInterval(checkHealth, 5000);

    // Cleanup function (important to prevent memory leaks when the component unmounts)
    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme: any) => theme.zIndex.drawer + 1 }}
        style={{ background: "#1D4A55" }}
      >
        <Toolbar
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ float: "left" }}>
              <img src="babyBender.png" width={"60px"} />
            </div>
            <div style={{ float: "left", marginTop: "18px" }}>
              <Link
                href="/"
                style={{
                  textDecoration: "none",
                  color: "black",
                  fontSize: "40px",
                  fontFamily: "robotFont",
                }}
              >
                ChatBot
              </Link>
            </div>
          </div>
          <div className="nav-elements">
            <ul>
              <li>
                <Link href="/about">About</Link>
              </li>
              <li>
                <Link href="/settings">Settings</Link>
              </li>
              <li>
                <Link href="/guide">Guide</Link>
              </li>
            </ul>
          </div>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        PaperProps={{
          sx: {
            backgroundColor: "#BDB7AB",
            color: "black",
          },
        }}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto", height: "100%" }}>
          <List>
            <Link href="/database" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>Database</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>
            <Link href="/chatRoom" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>Chat Room</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>
            <Link href="/settings" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>Settings</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>
            <Link href="/about" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>About</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>

            <ListItem>
              <ListItemButton>
                <ListItemIcon>{serverStatus}</ListItemIcon>
              </ListItemButton>
            </ListItem>
          </List>

          <List
            style={{
              position: "fixed",
              bottom: "0px",
              width: "9.3%",
            }}
          >
            <Divider sx={{ borderBottomWidth: 3 }} />
            <Link href="/contact" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>Contact</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>
          </List>
        </Box>
      </Drawer>
    </>
  );
};

export default Wrapper;
