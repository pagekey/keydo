'use client'

import { Button, Title } from "@mantine/core";
import { invoke } from '@tauri-apps/api/tauri';
import { useState } from "react";


export default function Home() {
  
  const handleNew = () => {
    invoke('project_new');
  };
  const handleOpen = () => {
    invoke('project_open');
  };

  return (
    <>
      <Title className='text-center pt-2'>KeyDo</Title>
      <div className='py-8 text-center'>
        Let's get things done.
      </div>
      <div className='flex w-full justify-around'>
        <Button variant='outline' color='red' onClick={handleNew}>New Project</Button>
        <Button variant='outline' onClick={handleOpen}>Open Project</Button>
      </div>
    </>
  )
}
