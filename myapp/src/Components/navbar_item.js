import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';

const NavbarItem = () => {
	return (
		<Navbar bg='dark' variant='dark' expand='lg'>
			<Navbar.Brand as={Link} to='/'>
				GoodReads
			</Navbar.Brand>
			<Navbar.Toggle aria-controls='basic-navbar-nav' />
			<Navbar.Collapse id='basic-navbar-nav'>
				<Nav className='mr-auto'>
					<Nav.Link as={Link} to='/get'>
						GET
					</Nav.Link>
					<Nav.Link as={Link} to='/post'>
						Post
					</Nav.Link>
					<Nav.Link as={Link} to='/delete'>
						Delete
					</Nav.Link>
					<Nav.Link as={Link} to='/update'>
						Update
					</Nav.Link>
					<Nav.Link as={Link} to='/vis/top-authors'>
						Author Visualizer
					</Nav.Link>
					<Nav.Link as={Link} to='/vis/top-books'>
						Book Visualizer
					</Nav.Link>
				</Nav>
			</Navbar.Collapse>
		</Navbar>
	);
};

export default NavbarItem;
