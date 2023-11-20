import { useNavigate } from "react-router-dom";
import { Button } from "semantic-ui-react";
import React from 'react';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

export function MainApp(){
    const nav = useNavigate();

     function handleOnClick(){
            nav("/detailspage");
    }

    return( <>
    <div className="flex bg-black h-screen grow justify-center items-center block justify-center items center">
        <div className="flex flex font-arial hover:outline outline-white outline-1 rounded-3xl p-2">
            <div className="text-white  text-7xl  m-5 mb-0">AutoEntry</div>
            <div className="flex grow justify-end"><button className="bg-black text-white  p-3 rounded-3xl outline-1 outline-white border-1 border-white m-5" onClick={handleOnClick}>
                <ArrowForwardIcon sx={{ fontSize: 45 }}/>
                </button></div>
        
        </div>
        
      
        </div>
    </>)
}