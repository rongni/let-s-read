import React from 'react';
import { Route, Switch } from 'react-router-dom';
import { GetForm } from './Components/get_book_author';
import { GetAllForm } from './Components/get_all_book_author';
import { DeleteForm } from './Components/delete_book_author';
import { PostBookForm } from './Components/post_book_form';
import NavbarItem from './Components/navbar_item';
import { PostAuthorForm } from './Components/post_author_form';
import { PutBookForm } from './Components/put_book_form';
import { PutAuthorForm } from './Components/put_author_form';
import { ScrapeForm } from './Components/get_scrape';
import { SearchForm } from './Components/get_search';
import { BookVisualizer } from './Components/vis_top_books';
import { AuthorVisualizer } from './Components/vis_top_authors';
import './App.css';

function App() {
	return (
		<div className='App'>
			<NavbarItem />
			<Switch>
				<Route exact path='/'>
					<p1>Search</p1>
					<SearchForm />
				</Route>
				<Route path='/get'>
					<span> </span>
					<p2>Get BOOK OR Author BY Id</p2>
					<GetForm />
					<p2>Get All BOOK OR Author</p2>
					<GetAllForm />
				</Route>
				<Route path='/post'>
					<p2>Post Author</p2>
					<PostAuthorForm />
					<p2>Post Book</p2>
					<PostBookForm />
					<p2>Scrape Book and Author</p2>
					<ScrapeForm />
				</Route>
				<Route path='/delete'>
					<span> </span>
					<p2>Delete Book or Author By ID</p2>
					<DeleteForm />
				</Route>
				<Route path='/update'>
					<span> </span>
					<p2>Update Book</p2>
					<PutBookForm />
					<span> </span>
					<p2>Update Author</p2>
					<PutAuthorForm />
				</Route>
				<Route exact path='/vis/top-books'>
					<p1> Top K Highest Rated books. </p1>
					<BookVisualizer />
				</Route>
				<Route exact path='/vis/top-authors'>
					<p1> Top K Highest Rated authorss. </p1>
					<AuthorVisualizer />
				</Route>
			</Switch>
		</div>
	);
}

export default App;
