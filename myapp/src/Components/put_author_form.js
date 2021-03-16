import React, { useState } from 'react';
import { Book } from './show';

export const PutAuthorForm = () => {
	const [result, setResult] = useState([]);
	const [putAuthor, setputAuthor] = useState({
		attribute: '',
		value: '',
		author_id: '',
	});

	function handleChange(evt) {
		evt.preventDefault();
		const value = evt.target.value;
		setputAuthor({
			...putAuthor,
			[evt.target.name]: value,
		});
	}

	function handleSubmit(event) {
		event.preventDefault();
		const dict = {};
		dict[putAuthor.attribute] = putAuthor.value;

		fetch(`/authors?author_id=${putAuthor.author_id}`, {
			method: 'PUT',
			body: JSON.stringify({
				dict,
			}),
		})
			.then((response) => response.json())
			.then((data) => setResult(data));
	}
	return (
		<>
			<div>
				<form onSubmit={handleSubmit}>
					<label>
						Upate Author Attribute
						<select
							name='attribute'
							onChange={handleChange}
							value={putAuthor.attribute}
						>
							<option value='name'>Name</option>
							<option value='author_url'>Author URL</option>
							<option value='rating'>Rating</option>
							<option value='rating_count'>Rating Count</option>
							<option value='review_count'>Review Count</option>
							<option value='image_url'>Image URL</option>
							<option value='related_authors'>Related Author</option>
							<option value='author_books'>Author Books</option>
						</select>
					</label>
					<input
						type='text'
						placeholder='Value'
						name='value'
						onChange={handleChange}
						value={putAuthor.value}
					/>
					<input
						type='text'
						placeholder='Author ID'
						name='author_id'
						value={putAuthor.author_id}
						onChange={handleChange}
					></input>
					<input type='submit'></input>
				</form>
			</div>
			<Book result={result} />
		</>
	);
};
