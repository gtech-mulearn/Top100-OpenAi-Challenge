import { useNavigate } from "react-router-dom";
import { Button } from "semantic-ui-react";
import React from 'react';

export function MainApp(){
    const nav = useNavigate();

     function handleOnClick(){
            nav("/detailspage");
    }

    return( <>\
    <div className="flex grow block justify-center items center">
        <div className="flex h-auto">
        <h1 >Event Manager</h1>
        <Button  onClick={handleOnClick}>continue...</Button>
        </div>
        </div>
    </>)
}