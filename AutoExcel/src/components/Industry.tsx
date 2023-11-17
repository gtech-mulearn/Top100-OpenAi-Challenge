import React, { useState,useEffect } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import '../styles/Industry.css';
import Backdrop from '@mui/material/Backdrop';


interface IndustryDialogProps {
 
  onClose: () => void;
}

const IndustryDialog: React.FC<IndustryDialogProps> = ({  onClose}) => {
  const [open, setOpen] = useState(true);
  const [industry, setIndustry] = useState('');

  ;

  const handleClose = () => {
    setOpen(false);
    onClose();
  };

  const handleIndustryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIndustry(event.target.value);
  };

  const handleSave = () => {
    localStorage.removeItem('industry');
    //onSave(industry);
    handleClose();
  };

  useEffect(() => {
    localStorage.removeItem('industry');
  }, []);

  return (
    <div>
      
      <Dialog open={open} onClose={handleClose}  PaperProps={{ style: { backgroundColor: '#9A8C98' } }} >
        <DialogTitle>Explain your bussiness in few words....</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            id="industry"
            label="Explain your bussiness in a few words?"
            type="text"
            fullWidth
            value={industry}
            onChange={handleIndustryChange}
          />
        </DialogContent>
        <DialogActions>
          <button onClick={handleSave} className='btn2'>
            Submit
          </button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default IndustryDialog;
