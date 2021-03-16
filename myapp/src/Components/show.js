import React from 'react';

export const Book = ({ result }) => {
	return (
		<>
			{Object.entries(result).map(([key, value]) => (
				<li key='{key}'>
					{key}: {value}
				</li>
			))}
		</>
	);
};
