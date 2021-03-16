import React, { useState } from 'react';
import { Book } from './show';

export const PostBookForm = () => {
	const [result, setResult] = useState([]);
	const [postBook, setPostBook] = useState({
		book_url: '',
		title: '',
		book_id: '',
		ISBN: '',
		author: '',
		author_url: '',
		rating: '',
		rating_count: '',
		review_count: '',
		image_url: '',
		similar_books: [],
	});

	function handleChange(evt) {
		const value = evt.target.value;
		setPostBook({
			...postBook,
			[evt.target.name]: value,
		});
	}

	function handleSubmit(event) {
		event.preventDefault();
		console.log(postBook);
		fetch(`/books`, {
			method: 'POST',
			body: JSON.stringify({
				postBook,
			}),
		})
			.then((response) => response.json())
			.then((data) => setResult(data));
	}

	return (
		<>
			<div>
				<form onSubmit={handleSubmit} method='POST'>
					<input
						type='text'
						placeholder='Book Url'
						name='book_url'
						onChange={handleChange}
						value={postBook.book_url}
					/>
					<input
						type='text'
						placeholder='Title'
						name='title'
						onChange={handleChange}
						value={postBook.title}
					/>
					<input
						type='text'
						placeholder='Book ID'
						name='book_id'
						onChange={handleChange}
						value={postBook.book_id}
					/>
					<input
						type='text'
						placeholder='ISBN'
						name='ISBN'
						onChange={handleChange}
						value={postBook.ISBN}
					/>
					<input
						type='text'
						placeholder='Author'
						name='author'
						onChange={handleChange}
						value={postBook.author}
					/>
					<input
						type='text'
						placeholder='Author URL'
						name='author_url'
						onChange={handleChange}
						value={postBook.author_url}
					/>
					<input
						type='text'
						placeholder='Rating'
						name='rating'
						onChange={handleChange}
						value={postBook.rating}
					/>
					<input
						type='text'
						placeholder='Rating Count'
						name='rating_count'
						onChange={handleChange}
						value={postBook.rating_count}
					/>
					<input
						type='text'
						placeholder='Review Count'
						name='review_count'
						onChange={handleChange}
						value={postBook.review_count}
					/>
					<input
						type='text'
						placeholder='Image Url'
						name='image_url'
						onChange={handleChange}
						value={postBook.image_url}
					/>
					<input
						type='array'
						placeholder='Similar Books'
						name='similar_books'
						onChange={handleChange}
						value={postBook.similar_books}
					/>
					<input type='submit' />
				</form>
			</div>
			<Book result={result} />
		</>
	);
};
