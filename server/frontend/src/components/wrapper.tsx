import * as React from "react";
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

//**This component is by default present on all pages*/
const Wrapper = () => {
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
            <Link href="/history" style={{ textDecoration: "none" }}>
              <ListItem>
                <ListItemButton>
                  <ListItemIcon>History</ListItemIcon>
                </ListItemButton>
              </ListItem>
            </Link>
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
