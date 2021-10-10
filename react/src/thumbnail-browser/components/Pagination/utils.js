export const defaultLabelDisplayedRows = ({
  from, to, count,
}) => `${from}-${to} av ${count !== -1 ? count : `mer enn ${to}`}`;

export const defaultRowsPerPageOptions = [8, 20, 50, 100, 250];

export const defaultLabelRowsPerPage = 'Antall per side';
