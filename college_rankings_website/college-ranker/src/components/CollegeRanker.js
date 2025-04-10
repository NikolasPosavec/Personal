import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Box, 
  TextField, 
  Button, 
  List, 
  ListItem, 
  ListItemText, 
  Typography,
  Paper,
  Divider
} from '@mui/material';

class College {
  constructor(name, size, cs_rank, campus_rating) {
    this.name = name;
    this.size = size;
    this.cs_rank = cs_rank;
    this.campus_rating = campus_rating;
  }

  score(weights, stat_ranges) {
    const normalize = (val, min_val, max_val) => {
      return (val - min_val) / (max_val - min_val) || 0;
    };

    const size_score = 1 - normalize(this.size, ...stat_ranges.size);
    const cs_score = 1 - normalize(this.cs_rank, ...stat_ranges.cs_rank);
    const campus_score = 1 - normalize(this.campus_rating, ...stat_ranges.campus);

    const total_weight = weights.size + weights.cs + weights.campus;
    if (total_weight === 0) return 0;

    const weighted_sum = (
      weights.size * size_score +
      weights.cs * cs_score +
      weights.campus * campus_score
    );

    return (weighted_sum / total_weight) * 3;
  }
}

const defaultColleges = [
  new College("Clemson", 21000, 80, 4),
  new College("UGA", 31000, 80, 4),
  new College("University of South Carolina", 27000, 110, 4),
  new College("Case Western Reserve", 5500, 71, 5),
  new College("Fairfield", 4400, 200, 5),
  new College("Miami University (Oxford)", 17000, 200, 4),
  new College("NC State", 26000, 51, 5),
  new College("Penn State", 47000, 39, 5),
  new College("Ohio State", 46000, 35, 4),
  new College("University of Delaware", 18500, 71, 6),
  new College("UMD", 30000, 16, 3),
  new College("Villanova", 7000, 150, 1),
  new College("Virginia Tech", 29000, 35, 1),
  new College("Pitt", 19000, 51, 4)
];

const getStatRanges = (colleges) => ({
  size: [Math.min(...colleges.map(c => c.size)), Math.max(...colleges.map(c => c.size))],
  cs_rank: [Math.min(...colleges.map(c => c.cs_rank)), Math.max(...colleges.map(c => c.cs_rank))],
  campus: [Math.min(...colleges.map(c => c.campus_rating)), Math.max(...colleges.map(c => c.campus_rating))]
});

const CollegeRanker = () => {
  const { currentUser, saveColleges } = useAuth();
  const [weights, setWeights] = useState({ size: 1, cs: 1, campus: 1 });
  const [rankedColleges, setRankedColleges] = useState([]);
  const [userColleges, setUserColleges] = useState([]);
  const [newCollege, setNewCollege] = useState({
    name: '',
    size: '',
    cs_rank: '',
    campus_rating: ''
  });

  useEffect(() => {
    if (currentUser?.colleges) {
      setUserColleges(currentUser.colleges);
    }
  }, [currentUser]);

  const rankColleges = () => {
    const allColleges = [...defaultColleges, ...userColleges];
    const statRanges = getStatRanges(allColleges);
    const ranked = [...allColleges].sort((a, b) => 
      b.score(weights, statRanges) - a.score(weights, statRanges)
    );
    setRankedColleges(ranked);
  };

  const handleWeightChange = (e) => {
    setWeights({
      ...weights,
      [e.target.name]: parseFloat(e.target.value) || 0
    });
  };

  const handleCollegeChange = (e) => {
    setNewCollege({
      ...newCollege,
      [e.target.name]: e.target.value
    });
  };

  const addCollege = () => {
    if (!newCollege.name || !newCollege.size || !newCollege.cs_rank || !newCollege.campus_rating) return;
    
    const college = new College(
      newCollege.name,
      parseInt(newCollege.size),
      parseInt(newCollege.cs_rank),
      parseInt(newCollege.campus_rating)
    );
    
    const updatedColleges = [...userColleges, college];
    setUserColleges(updatedColleges);
    if (currentUser) {
      saveColleges(updatedColleges);
    }
    setNewCollege({
      name: '',
      size: '',
      cs_rank: '',
      campus_rating: ''
    });
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" gutterBottom>
        College Ranker
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Weight Settings
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <TextField
            label="Size Weight"
            name="size"
            type="number"
            value={weights.size}
            onChange={handleWeightChange}
            fullWidth
          />
          <TextField
            label="CS Rank Weight"
            name="cs"
            type="number"
            value={weights.cs}
            onChange={handleWeightChange}
            fullWidth
          />
          <TextField
            label="Campus Rating Weight"
            name="campus"
            type="number"
            value={weights.campus}
            onChange={handleWeightChange}
            fullWidth
          />
        </Box>
        <Button variant="contained" onClick={rankColleges} fullWidth>
          Rank Colleges
        </Button>
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Add Your College
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            label="College Name"
            name="name"
            value={newCollege.name}
            onChange={handleCollegeChange}
            fullWidth
          />
          <TextField
            label="Size"
            name="size"
            type="number"
            value={newCollege.size}
            onChange={handleCollegeChange}
            fullWidth
          />
        </Box>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            label="CS Rank"
            name="cs_rank"
            type="number"
            value={newCollege.cs_rank}
            onChange={handleCollegeChange}
            fullWidth
          />
          <TextField
            label="Campus Rating (1=best, 10=worst)"
            name="campus_rating"
            type="number"
            value={newCollege.campus_rating}
            onChange={handleCollegeChange}
            fullWidth
          />
        </Box>
        <Button 
          variant="contained" 
          onClick={addCollege} 
          fullWidth
          disabled={!currentUser}
        >
          {currentUser ? "Add College" : "Please login to add colleges"}
        </Button>
      </Paper>

      {rankedColleges.length > 0 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Ranked Colleges
          </Typography>
          <List>
            {rankedColleges.map((college, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={`${index + 1}. ${college.name}`}
                  secondary={`Score: ${college.score(weights, getStatRanges([...defaultColleges, ...userColleges])).toFixed(2)}/3.00`}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};

export default CollegeRanker;