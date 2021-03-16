import React, { useState } from 'react';
import { Book } from './show';

export const PutBookForm = () => {
	const [result, setResult] = useState([]);
	const [putBook, setPutBook] = useState({
		attribute: '',
		value: '',
		book_id: '',
	});

	function handleChange(evt) {
		evt.preventDefault();
		const value = evt.target.value;
		setPutBook({
			...putBook,
			[evt.target.name]: value,
		});
	}

	function handleSubmit(event) {
		event.preventDefault();
		const dict = {};
		dict[putBook.attribute] = putBook.value;

		fetch(`/books?book_id=${putBook.book_id}`, {
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
						Upate Book Attribute
						<select
							name='attribute'
							onChange={handleChange}
							value={putBook.attribute}
						>
							<option value='book_url'>Book URL</option>
							<option value='title'>Title</option>
							<option value='ISBN'>ISBN</option>
							<option value='author'>Author</option>
							<option value='author_url'>Author URL</option>
							<option value='rating'>Rating</option>
							<option value='rating_count'>Rating Count</option>
							<option value='review_count'>Review Count</option>
							<option value='image_url'>Image URL</option>
							<option value='similar_books'>Similar Books</option>
						</select>
					</label>
					<input
						type='text'
						placeholder='Value'
						name='value'
						onChange={handleChange}
						value={putBook.value}
					/>
					<input
						type='text'
						placeholder='Book ID'
						name='book_id'
						value={putBook.book_id}
						onChange={handleChange}
					></input>
					<input type='submit'></input>
				</form>
			</div>
			<Book result={result} />
		</>
	);
};
