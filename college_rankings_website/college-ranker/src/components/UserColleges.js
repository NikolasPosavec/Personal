import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Box, Typography, List, ListItem, ListItemText, Button } from '@mui/material';

const UserColleges = () => {
  const { currentUser, saveColleges } = useAuth();
  const [userColleges, setUserColleges] = useState([]);

  useEffect(() => {
    if (currentUser?.colleges) {
      setUserColleges(currentUser.colleges);
    }
  }, [currentUser]);

  const removeCollege = (index) => {
    const updatedColleges = [...userColleges];
    updatedColleges.splice(index, 1);
    setUserColleges(updatedColleges);
    saveColleges(updatedColleges);
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        My Colleges
      </Typography>
      {userColleges.length === 0 ? (
        <Typography>You haven't added any colleges yet.</Typography>
      ) : (
        <List>
          {userColleges.map((college, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={college.name}
                secondary={`Size: ${college.size}, CS Rank: ${college.cs_rank}, Campus Rating: ${college.campus_rating}`}
              />
              <Button 
                variant="outlined" 
                color="error"
                onClick={() => removeCollege(index)}
              >
                Remove
              </Button>
            </ListItem>
          ))}
        </List>
      )}
    </Box>
  );
};

export default UserColleges;