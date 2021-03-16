import React, { useState } from 'react';
import { Book } from './show';

export function GetForm(props) {
	const [id, setId] = useState('');
	const [field, setField] = useState('/books?book_id');
	const [res, setRes] = useState([]);

	const handleSubmit = (evt) => {
		evt.preventDefault();
		fetch(`${field}=${id}`, {
			mode: 'no-cors',
			method: 'GET',
		})
			.then((response) => response.json())
			.then((data) => setRes(data));
		setId('');
	};
	return (
		<div>
			<form onSubmit={handleSubmit}>
				<label>
					ID:
					<input
						type='text'
						name='book_id'
						value={id}
						onChange={(e) => setId(e.target.value)}
					/>
				</label>
				<input type='submit' value='Submit' />
				<select name='field' onChange={(e) => setField(e.target.value)}>
					<option value='/books?book_id'>Book</option>
					<option value='/authors?author_id'>Author</option>
				</select>
			</form>
			<Book result={res} />
		</div>
	);
}
