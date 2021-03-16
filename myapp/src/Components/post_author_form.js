import React, { useState } from 'react';
import { Book } from './show';

export const PostAuthorForm = () => {
	const [result, setResult] = useState([]);
	const [postAuthor, setpostAuthor] = useState({
		name: '',
		author_url: '',
		author_id: '',
		rating: '',
		rating_count: '',
		review_count: '',
		image_url: '',
		related_authors: [],
		author_books: [],
	});

	function handleChange(evt) {
		const value = evt.target.value;
		setpostAuthor({
			...postAuthor,
			[evt.target.name]: value,
		});
	}

	function handleSubmit(event) {
		event.preventDefault();
		console.log(postAuthor);
		fetch(`/authors`, {
			method: 'POST',
			body: JSON.stringify({
				postAuthor,
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
						placeholder='Name'
						name='name'
						onChange={handleChange}
						value={postAuthor.name}
					/>
					<input
						type='text'
						placeholder='Author Url'
						name='author_url'
						onChange={handleChange}
						value={postAuthor.author_url}
					/>
					<input
						type='text'
						placeholder='Rating'
						name='rating'
						onChange={handleChange}
						value={postAuthor.rating}
					/>
					<input
						type='text'
						placeholder='Rating Count'
						name='rating_count'
						onChange={handleChange}
						value={postAuthor.rating_count}
					/>
					<input
						type='text'
						placeholder='Review Count'
						name='review_count'
						onChange={handleChange}
						value={postAuthor.review_count}
					/>
					<input
						type='text'
						placeholder='Image Url'
						name='image_url'
						onChange={handleChange}
						value={postAuthor.image_url}
					/>
					<input
						type='array'
						placeholder='Related Authors'
						name='related_authors'
						onChange={handleChange}
						value={postAuthor.related_authors}
					/>
					<input
						type='array'
						placeholder='Author Books'
						name='author_books'
						onChange={handleChange}
						value={postAuthor.author_books}
					/>
					<input type='submit' />
				</form>
			</div>
			<Book result={result} />
		</>
	);
};
