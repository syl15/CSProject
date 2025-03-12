import * as React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useState } from 'react';
import Searchbar from './Searchbar';
import './Navbar.css'
// import SearchIcon from '@mui/icons-material/Search';

const drawerWidth = 240;
const navItems = ['Overview', 'Past Disasters'];

export default function Navbar(props) {
  const { window } = props;
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen((prevState) => !prevState);
  };

  const dropDownMenu = (
    <Box onClick={handleDrawerToggle}>
      {/* <Typography>
        Disaster Sentiment Tracker
      </Typography>
      <div className="bg-black">testing</div> */}
      {/* <Divider /> */}
      {/* <List>
        {navItems.map((item) => (
          <ListItem key={item} disablePadding>
            <ListItemButton>
              <ListItemText primary={item} />
            </ListItemButton>
          </ListItem>
        ))}
      </List> */}
      {/* <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search…"
              inputProps={{ 'aria-label': 'search' }}
            />
       </Search> */}
    </Box>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    <Box
    
    >
      {/* <CssBaseline/> */}
      <AppBar component="nav"
        sx={{ 
            p:1,
            bgcolor: '#fff',
            boxShadow: 0,
            borderBottom:1,
            borderColor: '#D4D4D4'    
        }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            
           >
            <MenuIcon sx={{ 
                display: { xs: 'block', md: 'none' },
                color:'#000' 
            }} />
            
          </IconButton>
          
          <Typography sx={{ 
            p:1,
            color: '#000',
            fontWeight: 800,
            }}>
            Disaster Sentiment Tracker
          </Typography>
          <Box sx={
            { display: { xs: 'none', md:'flex'}, 
                pl: 5,
            }
            }>
            {navItems.map((item) => (
              <Button key={item} 
              sx={{ 
                color: '#000', 
                px: 2,
                mx:1,
                border:1.3,
                borderColor: '#D4D4D4',
                borderRadius: '5px',
                textTransform: 'none'
              }}>

                {item}
              </Button>
            ))}
            <Searchbar/>
          </Box>
          
        </Toolbar>
      </AppBar>
      <nav>
        <Drawer
          container={container}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {dropDownMenu}
        </Drawer>
      </nav>
    </Box>
  );
}
