import React, { useState } from 'react';
import { Book } from './show';
import * as d3 from 'd3';

export function BookVisualizer(props) {
	const [topK, setTopK] = useState('');
	// const [field, setField] = useState('/vis/top-books');
	const [res, setRes] = useState([]);

	const handleSubmit = (evt) => {
		evt.preventDefault();
		fetch(`/vis/top-books`, {
			mode: 'no-cors',
			method: 'GET',
		})
			.then((response) => response.json())
			.then((data) => componentDidMount(data));
		setTopK('');
	};
	const show = (data) => {
		console.log(data);
		var bookTitle = [];
		var bookRate = [];
		var count = 0;

		// }
		for (let k in data) {
			if (count < topK) {
				bookTitle[count] = k + ' : ' + data[k];
				bookRate[count] = data[k];
				count++;
			}
		}

		const svg = d3
			.select('body')
			.append('svg')
			.attr('width', 700)
			.attr('height', 10000)
			.style('margin-left', 100);

		svg
			.selectAll('rect')
			.data(bookRate)
			.enter()
			.append('rect')
			.attr('x', (d, i) => 200 - 20 * d)
			.attr('y', (d, i) => 25 + i * 100)
			.attr('width', (d, i) => d * 20)
			.attr('height', 65)
			.attr('fill', 'black');

		svg
			.selectAll('text')
			.data(bookTitle)
			.enter()
			.append('text')
			.text((d) => d)
			.attr('x', (d, i) => 50)
			.attr('y', (d, i) => 13 + i * 100);
	};

	const componentDidMount = (data) => {
		console.log(data);
		show(data);
	};

	return (
		<div>
			{/* <div id={'#' + 2}></div> */}
			<form onSubmit={handleSubmit}>
				<label>
					K:
					<input
						type='int'
						name='Top_K'
						value={topK}
						onChange={(e) => setTopK(e.target.value)}
					/>
				</label>
				<input type='submit' value='Submit' />
			</form>
			{/* <Book result={res} /> */}
		</div>
	);
}
