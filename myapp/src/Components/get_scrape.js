import React, { useState } from 'react';
import { Book } from './show';

export const ScrapeForm = () => {
	const [result, setResult] = useState([]);
	const [scrape, setScrape] = useState('');

	function handleChange(evt) {
		const value = evt.target.value;
		setScrape(value);
	}

	function handleSubmit(event) {
		event.preventDefault();
		fetch(`/scrape?attr=${scrape}`, {
			method: 'POST',
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
						placeholder='URL'
						name='url'
						value={scrape}
						onChange={handleChange}
					></input>
					<input type='submit'></input>
				</form>
			</div>
			<p1>Success</p1>
		</>
	);
};
