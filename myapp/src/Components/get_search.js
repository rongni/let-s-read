import { Book } from './show';
import React, { useState } from 'react';

export const SearchForm = () => {
	const [result, setResult] = useState([]);
	const [search, setSearch] = useState('');

	function handleChange(evt) {
		const value = evt.target.value;
		setSearch(value);
	}

	function handleSubmit(event) {
		event.preventDefault();
		fetch(`/search?q=${search}`, {
			method: 'GET',
		})
			.then((response) => response.json())
			.then((data) => setResult(data));
	}
	return (
		<>
			<div>
				<form onSubmit={handleSubmit}>
					<input
						type='text'
						placeholder='Query'
						name='query'
						value={search}
						onChange={handleChange}
					></input>
					<input type='submit'></input>
				</form>
			</div>
			<Book result={result} />
		</>
	);
};
