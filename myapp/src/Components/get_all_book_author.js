import React, { useState } from 'react';
import { Book } from './show';

export function GetAllForm(props) {
	const [field, setField] = useState('/allbooks?limit');
	const [res, setRes] = useState([]);
	const [limit, setLimit] = useState('');
	const handleSubmit = (evt) => {
		evt.preventDefault();
		fetch(`${field}=${limit}`, {
			mode: 'no-cors',
			method: 'GET',
		})
			.then((response) => response.json())
			.then((data) => setRes(data));
	};
	return (
		<div>
			<form onSubmit={handleSubmit}>
				<select name='field' onChange={(e) => setField(e.target.value)}>
					<option value='/allbooks?limit'>Book</option>
					<option value='/allauthors?limit'>Author</option>
				</select>
				<input
					type='text'
					name='limit'
					value={limit}
					placeholder='Limit'
					onChange={(e) => setLimit(e.target.value)}
				/>
				<input type='submit' value='Submit' />
			</form>
			<Book result={res} />
		</div>
	);
}
