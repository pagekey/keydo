import { Button, Table, Title } from "@mantine/core";
import { invoke } from "@tauri-apps/api";
import { useEffect, useState } from "react";

interface Project {
    name: string
    next_action: string
    updated: string
}

export default function FolderView() {
    const [projects, setProjects] = useState<Project[]>([]);
    useEffect(() => {
        setTimeout(() => {
            setProjects([
                {
                    name: 'my project',
                    next_action: 'open phonebook',
                    updated: '2024-03-29',
                },
            ]);
        }, 500);
    }, []);

    const handleNewProject = () => {
        invoke('project_new');
    }
    return (
        <>
            <Title>KeyDo - Folder</Title>
            <div>
                <Button variant='outline' onClick={handleNewProject}>New Project</Button>
            </div>
            <Title order={2}>Projects</Title>
            <Table>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th>Name</Table.Th>
                        <Table.Th>Next Action</Table.Th>
                        <Table.Th>Updated</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                    {projects.map((project) => {
                        return (
                            <Table.Tr>
                                <Table.Td>
                                    {project.name}
                                </Table.Td>
                                <Table.Td>
                                    {project.next_action}
                                </Table.Td>
                                <Table.Td>
                                    {project.updated}
                                </Table.Td>
                            </Table.Tr>
                        )
                    })}
                </Table.Tbody>
            </Table>
        </>
    )
}
